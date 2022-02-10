from logging import error

import sys

sys.path.append("../utils")

from utils.mutation_tools import delete_none

import xml.etree.ElementTree as ET
import xmltodict


def convert_bool_to_yes(_dict):
    for k, data in _dict.items():
        if isinstance(data, dict):
            convert_bool_to_yes(data)
        else:
            if data is True:
                _dict[k] = "yes"
    return _dict


class Transformation:
    def __init__(self, pipeline) -> None:
        self.hooks = []
        self.hook_data = []
        self.pipeline = pipeline
        self.pipeline.append(convert_bool_to_yes)

    def transform(self, schema, input_data):
        # convert to dictionary bcuz it's much easier to work with

        print(input_data)
        validated = schema(**input_data).dict()
        if self.pipeline:
            generated_data = None
            for permutation in self.pipeline:
                if generated_data is None:
                    data = validated
                else:
                    data = generated_data
                generated_data = permutation(data)

                if not isinstance(generated_data, dict):
                    error("Each permuation Must return dictionary")

            return generated_data

        else:
            return validated


class HookAdapter:
    def __init__(self, hooks) -> None:
        self.hooks = hooks
        self.hook_data = []

    def process_hook(self, generated_data):
        if self.hooks:
            for hook in self.hooks:
                pin = hook(generated_data)
                print("PINCO", pin)
                if isinstance(pin, list):
                    self.hook_data.extend(pin)
                else:
                    self.hook_data.append(pin)
        return generated_data


class XmlTranslator:
    def __init__(self, root, dictionary_data) -> None:
        assert isinstance(
            dictionary_data, dict
        ), "XmlTranslator only accepts dictionary"
        self.root = root
        self.data = dictionary_data
        self.translated = None

    def translate(self):
        try:
            res = xmltodict.unparse(
                {self.root: self.data}, pretty=False
            )
            assert res is not None
            self.translated = ET.fromstring(res)
        except Exception as e:
            raise TranslateError(e, self.data, self.root)
        return self

    # mutate inner xml data
    def inject(self, xml_data):
        # print("INJECTING XML : ", self.root)

        assert (
            self.translated is not None
        ), "xml must be translated before injecting the xml element"
        translated = self.translated
        print("TRAN", ET.tostring(translated))
        for dt in xml_data:
            print("EACH DATA", dt)
            if isinstance(dt, dict):
                injecting_location = translated.find(dt["location"])
                if injecting_location is None:
                    raise Exception(
                        "Invalid Location !! \n Location:{}",
                        dt["location"],
                    )
                injecting_location.insert(0, dt["data"])
            else:
                translated.insert(1, dt)

    def result(self):
        return self.translated


class TranslateError(Exception):
    def __init__(self, e, data=None, root=None) -> None:
        self.data = data
        self.root = root
        self.error = e

    def __str__(self) -> str:
        print(
            "\nDATA INPUT :{} \nRoot Input: {} \n".format(
                self.data,
                self.root,
            )
        )
        msg = "Unable to translate!! encountered unexpected error! "
        return "{}\nXML ERROR : {}".format(msg, self.error)


class TranslateSchema:
    # pipeline: list = []
    # hooks: list = []
    # schema: dict
    # data: dict

    def __init__(self, schema, data) -> None:
        self.pipeline = []
        self.hooks = []
        self.schema = schema
        self.data = data

        self.transformer_builder = lambda: Transformation(
            self.pipeline
        ).transform(self.schema, self.data)

        self.hook_adapter_builder = lambda: HookAdapter(
            hooks=self.hooks
        )
        super()

    def inject_mutations(self, mutation_pipeline):
        self.pipeline = mutation_pipeline
        return self

    # hook will convert generated_data into xml
    # this xml will be append at the end of pipeline!

    def hook(self, hooks):
        self.hooks = hooks
        return self
        # self.hooks

    def call(self, root) -> ET.Element:
        transformed_data = self.transformer_builder()
        hook_adapter = self.hook_adapter_builder()

        # afterhook = Transformer.transform(self.pipeline, self.hook)
        afterhook = hook_adapter.process_hook(transformed_data)
        res = XmlTranslator(root, afterhook).translate()

        # xmlTransformed = ET.fromstring(
        #     xmltodict.unparse({root: afterhook}, pretty=False)
        # )
        res.inject(hook_adapter.hook_data)

        return res.result()


# # output : name of output file
# class CreateXmlService:
#     def __init__(self, rootname, schema) -> None:
#         self.rootname = rootname
#         self.schema = schema

#     def make_to_xml(self, output):
#         name = self.rootname
#         make = utils.CreateXmlAccessService(
#             outputTarget=output, root=name
#         )
#         o = make.call()

#         self.configElement = o["rootElement"]
#         self.targetFd = o["targetFd"]
#         self.root = o["rootElement"]
#         return self

#     def create(self, configs):
#         validated = utils.validate_field(self.schema, configs)
#         create = utils.CreateElementFactory(self.root)
#         create.call(None, validated)
#         return self

#     def writeToFile(self):
#         utils.CreateDataService(self.targetFd, self.root).call()


# class MakeTranslation:
#     def __init__(self, kind, schema):
#         self.xml = CreateXmlService(kind, schema)

#     def __call__(self, input, output_path) -> None:
#         self.xml.make_to_xml(output_path)
#         self.xml.create(input)
#         self.xml.writeToFile()

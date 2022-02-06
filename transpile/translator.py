from logging import error
import utils
import dataclasses
import xml.etree.ElementTree as ET
import xmltodict


@dataclasses.dataclass
class CreateSchema:
    root: str
    pipeline: list
    schema: dict
    hooks: list
    hook_data: list

    def __init__(self, schema, data) -> None:
        self.pipeline = []
        self.data = data
        self.schema = schema
        self.hooks = []
        self.hook_data = []

    def permuate(self, permutation):
        self.pipeline = permutation
        return self

    # hook will convert generated_data into xml
    # this xml will be append at the end of pipeline!

    def hook(self, hooks):
        self.hooks = hooks
        return self
        # self.hooks

    def transform(self):
        validated = utils.validate_field(self.schema, self.data)

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

    def process_hook(self):
        generated_data = self.transform()
        if self.hooks:
            for hook in self.hooks:
                pin = hook(generated_data)
                if isinstance(pin, list):
                    self.hook_data.extend(pin)
                else:
                    self.hook_data.append(pin)
        return generated_data

    def call(self, root):
        afterhook = self.process_hook()

        xmlTransformed = ET.fromstring(
            xmltodict.unparse({root: afterhook}, pretty=False)
        )

        for dt in self.hook_data:
            if isinstance(dt, dict):
                bruh = xmlTransformed.find(dt["location"])
                bruh.insert(0, dt["data"])
            else:
                xmlTransformed.insert(1, dt)

        return xmlTransformed


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

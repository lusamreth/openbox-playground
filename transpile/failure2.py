from types import LambdaType
import xml.etree.ElementTree as ET

print

depth_record = []
debuggin_matrices = []
depths = []
root_index = []
access_count_record = []
pine_tree = []


def detect_first_element(buffer):
    if len(buffer) == 1 and buffer:
        First = buffer[0]
        print("FIRST", First)
        First = None
        return [First]


def branch_calculator(buffer, count):
    # we can calculate the root by count + curr_len

    if len(buffer) == 0:
        return

    # print("COUNT COUNT", count, buffer)

    depths.append(len(buffer))
    last = len(depths) - 1

    curr_len = depths[last]
    prev_len = depths[last - 1]

    # print("the last last", curr_len, count)

    # noted that if curr_len is equal to prev_len it means
    # the start of a new tree !
    padding = 0

    if curr_len == prev_len and prev_len != 0:

        padding = 0

    branch = depth_record[prev_len - padding : curr_len]
    return branch


trees = []
treesdu = {}


def last_one(a, stepback=1):
    if len(a) == 0:
        return None
    return a[len(a) - stepback]


def get_indx():
    apen = None
    if last_one(root_index):
        apen = last_one(root_index)
    else:
        apen = 0
        # print("+++", root_index)
    return apen


def detect_depth_change(depth):
    le = len(depth)
    if le == 0:
        return False
    curr = depth[le - 1]
    prev = depth[le - 2]
    return curr == prev


prev = 0


class Detective:
    def __init__(self) -> None:
        self.prev = 0

    def detect_change(self, root_parent_ele):
        le = len(root_parent_ele)
        if le > self.prev:
            self.prev = le
            return True
        return False


D = Detective()
P = Detective()


class Appendage:
    def __init__(self) -> None:
        self.cux = 0

    def append(self):
        pass


cux = [0]
CALLS = [False, False]

pine_keys = []


def record_pine(indx, val):
    pine_tree.append({depth_record[indx]: val})
    pine_keys.append(depth_record[indx])


def extract_frist():
    if depth_record and not CALLS[1]:
        CALLS[1] = True


def produce_element(branch, k, v):
    super_slice = branch

    super_slice.extend([k])
    b = branch_to_xml(super_slice)
    b["tail"].text = v
    return b


Temp = []


def scanner(branch, k, v):
    s, e = root_index[cux[0]], last_one(root_index)
    print("FROM SCANNER")
    # super_slice = depth_record[s:e]
    main_root = depth_record[s]
    branchElement = produce_element(branch, k, v)
    # print("THIS BRANCH ELEMENT", branchElement)
    cux[0] += 1
    ox = last_one(root_index)
    parent = depth_record[last_one(root_index)]

    record_pine(ox, branchElement)
    # print(
    #     s,
    #     e,
    #     main_root,
    #     last_one(root_index),
    #     root_index,
    #     depth_record,
    # )


EBOCache = []

RMB = [0]


def new_append(branch, k, v, access_count):
    detect_root = D.detect_change(root_index)
    isFirstParent = detect_root and not CALLS[0]

    if isFirstParent and TempCache:
        record_pine(0, 0)
        TempCache.pop()
        CALLS[0] = True

    if Temp:
        meet_new_root = detect_root and branch
        if meet_new_root:
            print("TEMPI", Temp, branch, pine_tree, pine_keys)
            RMB[0] += 1
            p = branch[0]

            pine_tree.append({p: 0})
            pine_keys.append(p)

        count = RMB[0]

        #         if count == 0:
        #         else:

        #             par = Temp[0]
        #             print("PAR PAR", par, Temp)

        par = Temp[0]

        print("TEMPII", par, Temp, count)
        if detect_root and branch:
            Temp.clear()

        # if len(Temp) > 1:
        # print("OGGI PAR", par, Temp, pine_keys)

        if len(pine_keys) == 1 and Temp:
            par = ET.Element(pine_keys[count])
            print("PAsi", pine_tree[count], Temp)
            for tmp in Temp:
                par.insert(0, tmp)

        pine_tree[count][pine_keys[count]] = {"root": par}
        print("EACH PINE", pine_tree, par, count)

    def adjusting(msg, root):
        if TempCache and TempCache[0] >= 1:
            APP = False
            if isinstance(root, dict) and not EBOCache:
                APP = True
                EBOCache.append(root)
                root = ET.tostring(root["root"])

            TempCache[0] -= 1

            print(
                msg,
                TempCache,
                last_one(pine_keys),
                root,
                EBOCache,
                k,
                v,
            )

            if APP:
                print("APPE", EBOCache, TempCache)

            return APP

    # bruh("OUTSIDEIT", "None")

    if EBOCache:
        if not branch:
            TempCache[0] -= 1

            RX = EBOCache[0]["root"]
            u = ET.Element(k)
            u.text = v
            RX.insert(0, u)

            print(
                "OUTSIDETEMp",
                TempCache,
                ET.tostring(RX),
            )
            print(pine_tree)
            if TempCache[0] == 0:
                EBOCache.pop()
                # Temp.append(RX)
                TempCache.pop()
                return
        else:
            print("Vahalla", branch)
        print("OUTSIDEyo", TempCache, EBOCache)
    else:
        if branch:
            print("DOFO", branch)

    if branch:
        branch.extend([k])
        root = branch_to_xml(branch)
        root["tail"].text = v

        APP = adjusting("INSIDE ", root)
        HALT = False

        if APP:
            print("INSIDE START OF NEW ROOT", EBOCache)
        if EBOCache and not APP:
            R = EBOCache[0]["root"]
            print("INSIDE_DDD", TempCache, root["root"], EBOCache)
            # print(
            #     "INSIDE",
            #     root,
            # )
            # R.insert(1,rootij)

            R.insert(0, root["root"])
            HALT = True

        if TempCache and TempCache[0] == 0:
            TempCache.pop()

        if TempCache == [] and EBOCache:
            EBOCache.pop()
        # if HALT:
        #     return

        print(
            "root : ",
            ET.tostring(root["root"]),
            EBOCache,
            HALT,
            last_one(depths, 2),
        )

        if not HALT:
            Temp.append(root["root"])
        return


# here


def combine_all_trees(trees):
    First = depth_record[0]
    for tree in trees:
        print(ET.tostring(tree))


# count-parameter : count the item that has dictionary dict type(zero index)
# we can use this to determine root

First = None
count = 0


prev = [0]
croptop = [False]
import copy

TempCache = []


def traverse_tree(
    dictionary, buffer=[], access_count=0, root="root"
):

    for k, v in dictionary.items():

        if isinstance(v, dict):
            v_len = len(v.items())
            print(v_len, v, k)

            if v_len > 1:
                TempCache.append(v_len)

            if len(buffer) == 0:
                if prev[0] == 0:
                    root_index.append(prev[0])
                else:
                    root_index.append(len(prev[0]))

            prev[0] = buffer
            # print("inner buffer", buffer)
            depth_record.append(k)

            traverse_tree(v, depth_record)
            access_count += 1
        else:

            branch = branch_calculator(buffer, access_count)

            # access_count_record.append(access_count)

            # print("BRANCh", branch)
            # careful: will cause branch mutation !!
            # must copy the branch if u want to preserve its original state
            # of the parsed dict !!

            debuggin_matrices.append(branch)
            new_append(copy.deepcopy(branch), k, v, access_count)
            # append_txt(branch, k, v)

            # if root is not None:
            #     print("KILO", k, v)
            #     print(ET.tostring(root))


def branch_to_xml(depth_arr):

    halt = False
    # print(depth_arr)
    counter = len(depth_arr)
    depth_arr.reverse()
    root = None
    prevElement = None

    while not halt:
        curr = depth_arr.pop()

        counter = counter - 1
        if counter == 0:
            halt = True

        if root is None:
            root = ET.Element(curr)
            continue

        if prevElement is None:
            prevElement = ET.SubElement(root, curr)
        else:
            prevElement = ET.SubElement(prevElement, curr)

        # print("branch:", curr, prevElement, ET.tostring(root))
    return {"root": root, "tail": prevElement}


def convert_xml(input):
    buffer = input

    root = None

    for p in buffer:
        if root is None:
            root = ET.Element(p)
        else:
            ET.SubElement(root, p)
    return root


# must handle 3 cases:
# 1. empty branch
# 2. None branch
# 3. Non_empty branch

# Same key won't be rendered
import dicttoxml

nested = {
    "bruh1": "11",
    # "bruh2": {"sada": 1},
    "DOTAC2": {"SDu": {"sda": "sda"}, "bru": {"SDA": "1"}},
    "hell": {
        "id": "1",
        "okabil": "100",
        "okabil11": "100",
        "okabil2": "100",
        "pp01": {
            "lkee-2": {"pico": {"pp": "100"}},
            # "bruh": "100",
            "lkee-1": {"bruha": "100"},
            "lkee-3": {"bruh": "100"},
        },
        "ppp04": {"pbg": "010", "pbx": "012"},
        "ppp03": {"pbg": "010", "pbx": "012"},
        "ppp02": {"pbo": {"lkee": "100"}, "1pbo": {"lkee": "100"}},
        "pda": "100",
    },
    "DOTAC": {"SD": {"dsad": "bru"}, "Sad": "sad"},
    "pita2": {
        "pb": {"lkee": "100"},
        "DOTAC32": {"SDx": {"sda": "sda"}},
    },
    "DONDA": "100",
    # problem after entering root it neglect the upper element
    "pita": {
        "certic32": {"bruh1": {"sdas": "10"}},
        "certic": {"bruh1": {"sdas": "10"}},
        "aa": {"bruh1": {"sdas": "10"}},
    },
    "bruh": "11",
}

# if branch is None : mean the root is the element parent
# if branch is empty : mean the last eleemnt of ceptic(index)

traverse_tree(nested, root="nested")
# for k, nest in nested.items():
#     if isinstance(nest, dict):
#         print(k)
#         traverse_tree(nest)
print(depth_record)
# print(depths)
# print(debuggin_matrices)
print(root_index)


def final_assembly():
    root = ET.Element("root", {})
    print(len(pine_tree) == len(pine_keys), pine_keys)
    for i, pine in enumerate(pine_tree):
        p = pine[pine_keys[i]]
        if p == 0:
            continue
            # continue
        root.insert(0, p["root"])
    print(ET.tostring(root))


# operate()
print(root_index)
# print(treesdu)
print(pine_tree)

br = dicttoxml.convert(nested)
final_assembly()
print(debuggin_matrices)
# combine_all_trees(trees)
# branch_to_xml(["app", "app1"])

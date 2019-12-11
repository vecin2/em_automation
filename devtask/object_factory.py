import lxml.etree as ET

def add_process_def_node(parent):
    attribs ={
            "appearsInHistory":"true",
            "cyclic":"false",
            "designNotes":"Undefined",
            "exceptionStrategy":"1",
            "icon":"",
            "isPrivate":"false",
            "logicalDatabaseConnection":"",
            "name":"EmptyProcess",
            "nested":"false",
            "pointOfNoReturn":"false",
            "transactionBehaviour":"TX_NOT_SUPPORTED",
            "version":"10",
            "waitOnChildren":"false"}
    return ET.SubElement(parent,"ProcessDefinition",attribs)

def new_process_def():
    root = ET.Element('PackageEntry')
    process_def = add_process_def_node(root)
    ET.SubElement(process_def,"StartNode",displayName="",name="",x="16",y="32")
    ET.SubElement(process_def,"EndNode",displayName="",name="",x="240",y="32")
    transition = ET.SubElement(process_def,"Transition",isExceptionTransition="false")
    ET.SubElement(transition,"StartNodeReference",name="")
    ET.SubElement(transition,"EndNodeReference",name="")
    graph_node_list = ET.SubElement(transition,"GraphNodeList",name="")
    ET.SubElement(graph_node_list,
                   "GraphNode",
                   icon="",
                   isLabelHolder="true",
                   label="",
                   name="",
                   x="128",
                   y="32")
    ET.SubElement(process_def,"BuilderInfo",name="")
    ET.SubElement(process_def,"TopicScope",defineTopicScope="false",name="")
    return ET.tostring(root,
                pretty_print=True,
                doctype='<!DOCTYPE ProcessDefinition [] >',
                encoding ="UTF-8",
                xml_declaration=True,
                ).decode("utf-8")


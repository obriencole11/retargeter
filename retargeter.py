import pymel.core as pmc
import pymel.core.datatypes as dt
import controltools
import logging

##############################
#      Private Methods       #
##############################

class _undoBlock(object):

    def __enter__(self):
        pmc.undoInfo(openChunk=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pmc.undoInfo(closeChunk=True)
        if exc_val is not None:
            pmc.undo()

def _bind(source, target, translate=False, rotate=False, snap=True, scale=10.0):

    # Create the nodes
    tNode = _createTranslateNode(scale)
    pmc.rename(tNode, target.shortName() + '_translateOffset')
    _connectToTarget(tNode, target)

    rNode = _createRotateNode(scale)
    pmc.rename(rNode, target.shortName() + '_rotateOffset')
    pmc.parent(rNode, tNode)

    # If a parent exists, parent it, otherwise parent to world
    if source.getParent() is not None:
        pmc.parent(tNode, source.getParent())
    else:
        pmc.parent(tNode, world=True)

    # Set the nodes default positions and reset them
    tNode.setTranslation(target.getTranslation(worldSpace=True), worldSpace=True)
    pmc.makeIdentity(tNode, translate=True, apply=True)
    rNode.setRotation(target.getRotation(worldSpace=True), worldSpace=True)
    pmc.makeIdentity(rNode, rotate=True, apply=True)

    # Connect the source to the nodes
    pmc.orientConstraint(source, tNode, mo=True)

    # Connect the binds to the target
    # pmc.pointConstraint(tOffset, target)
    pmc.parentConstraint(rNode, target, mo=True)

    # Lock and hide the controls we don't want modified
    pmc.setAttr(tNode.rotate, channelBox=False, keyable=False, lock=True)
    pmc.setAttr(rNode.translate, channelBox=False, keyable=False, lock=True)
    pmc.setAttr(tNode.scale, channelBox=False, keyable=False, lock=True)
    pmc.setAttr(rNode.scale, channelBox=False, keyable=False, lock=True)

def _connectToTarget(node, target):

    # Add message attributes to the node and its target
    pmc.addAttr(node, ln='bindTarget', at='message')
    pmc.addAttr(target, ln='bindNode', at='message')

    # Connect the attributes
    pmc.connectAttr(node.bindTarget, target.bindNode)

def _findBindNodes():

    # Grab a list of every bind node in the scene
    return [obj for obj in pmc.ls(dag=True) if pmc.hasAttr(obj, 'bindTarget', checkShape=False)]

def _findBindTargets():

    # Grab all the bind nodes, and create a list of their targets
    return [node.bindTarget for node in _findBindNodes()]

def _createTranslateNode(scale=1.0):

    # Create the node and set its base size
    node = controltools.create_control_curve_from_data(CUBE_CURVEDATA)
    controltools.scale_curve(scale,scale,scale, node)

    # Color the node
    for shape in node.getShapes():
        pmc.setAttr(shape.overrideColorRGB, dt.Color(1,1,0))
        pmc.setAttr(shape.overrideRGBColors, True)
        pmc.setAttr(shape.overrideEnabled, True)

    return node

def _createRotateNode(scale=1.0):

    # Create the node and set its base size
    node = controltools.create_control_curve_from_data(OCTO_CURVEDATA)
    controltools.scale_curve(scale/2, scale/2, scale/2, node)

    # Color the node
    for shape in node.getShapes():
        pmc.setAttr(shape.overrideColorRGB, dt.Color.blue)
        pmc.setAttr(shape.overrideRGBColors, True)
        pmc.setAttr(shape.overrideEnabled, True)

    return node

def _removeNode(node):

    target = pmc.getAttr(node.bindTarget)
    pmc.deleteAttr(target.bindNode)
    pmc.deleteAttr(node.bindTarget)

    pmc.delete(node)


##############################
#      Public Methods       #
##############################

def bakeBindTargets():

    # Grab a list of all targets
    targets = _findBindTargets()

    if len(targets) > 0:

        # Grab the start and end frame
        start = pmc.playbackOptions(ast=True, q=True)
        end = pmc.playbackOptions(aet=True, q=True)

        print start
        print end

        # Bake the targets
        pmc.bakeResults(targets, t=(start, end), simulation=True)

        # Delete all the baked nodes
        for node in _findBindNodes():
            _removeNode(node)

    else:
        logging.warning('No Bind Nodes in scene')

def selectBindNodes():

    nodes = _findBindNodes()

    if len(nodes) > 0:

        # First clear the selection
        pmc.select(clear=True)

        # Then select all bind nodes
        pmc.select(nodes)

    else:
        logging.warning('No bind nodes to select')

def removeSelectedNodes():

    nodes = [obj for obj in pmc.selected() if pmc.hasAttr(obj, 'bindTarget')]

    if len(nodes) > 0:
        for node in nodes:
            _removeNode(node)
    else:
        logging.warning('No valid nodes selected')

def selectBindTargets():

    targets = _findBindTargets()

    if len(targets) > 0:

        # First clear the selection
        pmc.select(clear=True)

        # Then select all bind targets
        pmc.select(targets)

    else:
        logging.warning('No targets to select')

def bindSelected(translate, rotate, snap, scale):

    # Grab the selection
    selection = pmc.selected()

    if len(selection) > 1:

        # Grab the selections we care about
        source = selection[0]
        target = selection[1]

        # Bind the targets
        with _undoBlock():
            _bind(source, target, translate=translate, rotate=rotate, snap=snap, scale=scale)

    else:
        logging.warning('Not enough targets')


##### Shapes #####

SPHERE_CURVEDATA = [
        {
            "knots": [
                -2.0,
                -1.0,
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0
            ],
            "cvs": [
                [
                    0.783611624891225,
                    4.798237340988468e-17,
                    -0.7836116248912238
                ],
                [
                    -1.2643170607829326e-16,
                    6.785732323110913e-17,
                    -1.108194187554388
                ],
                [
                    -0.7836116248912243,
                    4.798237340988471e-17,
                    -0.7836116248912243
                ],
                [
                    -1.108194187554388,
                    1.966335461618786e-32,
                    -3.21126950723723e-16
                ],
                [
                    -0.7836116248912245,
                    -4.7982373409884694e-17,
                    0.783611624891224
                ],
                [
                    -3.3392053635905195e-16,
                    -6.785732323110915e-17,
                    1.1081941875543881
                ],
                [
                    0.7836116248912238,
                    -4.798237340988472e-17,
                    0.7836116248912244
                ],
                [
                    1.108194187554388,
                    -3.644630067904792e-32,
                    5.952132599280585e-16
                ],
                [
                    0.783611624891225,
                    4.798237340988468e-17,
                    -0.7836116248912238
                ],
                [
                    -1.2643170607829326e-16,
                    6.785732323110913e-17,
                    -1.108194187554388
                ],
                [
                    -0.7836116248912243,
                    4.798237340988471e-17,
                    -0.7836116248912243
                ]
            ],
            "degree": 3
        },
        {
            "knots": [
                -2.0,
                -1.0,
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0
            ],
            "cvs": [
                [
                    4.7982373409884756e-17,
                    0.7836116248912238,
                    -0.783611624891225
                ],
                [
                    -7.74170920797604e-33,
                    1.108194187554388,
                    1.2643170607829326e-16
                ],
                [
                    -4.798237340988471e-17,
                    0.7836116248912243,
                    0.7836116248912243
                ],
                [
                    -6.785732323110913e-17,
                    3.21126950723723e-16,
                    1.108194187554388
                ],
                [
                    -4.7982373409884725e-17,
                    -0.783611624891224,
                    0.7836116248912245
                ],
                [
                    -2.0446735801084019e-32,
                    -1.1081941875543881,
                    3.3392053635905195e-16
                ],
                [
                    4.798237340988468e-17,
                    -0.7836116248912244,
                    -0.7836116248912238
                ],
                [
                    6.785732323110913e-17,
                    -5.952132599280585e-16,
                    -1.108194187554388
                ],
                [
                    4.7982373409884756e-17,
                    0.7836116248912238,
                    -0.783611624891225
                ],
                [
                    -7.74170920797604e-33,
                    1.108194187554388,
                    1.2643170607829326e-16
                ],
                [
                    -4.798237340988471e-17,
                    0.7836116248912243,
                    0.7836116248912243
                ]
            ],
            "degree": 3
        },
        {
            "knots": [
                -2.0,
                -1.0,
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0
            ],
            "cvs": [
                [
                    0.783611624891225,
                    0.7836116248912238,
                    0.0
                ],
                [
                    -1.2643170607829326e-16,
                    1.108194187554388,
                    0.0
                ],
                [
                    -0.7836116248912243,
                    0.7836116248912243,
                    0.0
                ],
                [
                    -1.108194187554388,
                    3.21126950723723e-16,
                    0.0
                ],
                [
                    -0.7836116248912245,
                    -0.783611624891224,
                    0.0
                ],
                [
                    -3.3392053635905195e-16,
                    -1.1081941875543881,
                    0.0
                ],
                [
                    0.7836116248912238,
                    -0.7836116248912244,
                    0.0
                ],
                [
                    1.108194187554388,
                    -5.952132599280585e-16,
                    0.0
                ],
                [
                    0.783611624891225,
                    0.7836116248912238,
                    0.0
                ],
                [
                    -1.2643170607829326e-16,
                    1.108194187554388,
                    0.0
                ],
                [
                    -0.7836116248912243,
                    0.7836116248912243,
                    0.0
                ]
            ],
            "degree": 3
        }
    ]

CUBE_CURVEDATA = [
        {
            "knots": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0,
                14.0,
                15.0
            ],
            "cvs": [
                [
                    0.5,
                    0.5,
                    0.5
                ],
                [
                    0.5,
                    0.5,
                    -0.5
                ],
                [
                    -0.5,
                    0.5,
                    -0.5
                ],
                [
                    -0.5,
                    0.5,
                    0.5
                ],
                [
                    0.5,
                    0.5,
                    0.5
                ],
                [
                    0.5,
                    -0.5,
                    0.5
                ],
                [
                    0.5,
                    -0.5,
                    -0.5
                ],
                [
                    0.5,
                    0.5,
                    -0.5
                ],
                [
                    -0.5,
                    0.5,
                    -0.5
                ],
                [
                    -0.5,
                    -0.5,
                    -0.5
                ],
                [
                    0.5,
                    -0.5,
                    -0.5
                ],
                [
                    -0.5,
                    -0.5,
                    -0.5
                ],
                [
                    -0.5,
                    -0.5,
                    0.5
                ],
                [
                    -0.5,
                    0.5,
                    0.5
                ],
                [
                    -0.5,
                    -0.5,
                    0.5
                ],
                [
                    0.5,
                    -0.5,
                    0.5
                ]
            ],
            "degree": 1
        }
    ]

OCTO_CURVEDATA = [
        {
            "knots": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.0,
                13.0
            ],
            "cvs": [
                [
                    0.0,
                    -2.220446049250313e-16,
                    1.0
                ],
                [
                    1.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    1.0,
                    2.220446049250313e-16
                ],
                [
                    0.0,
                    -2.220446049250313e-16,
                    1.0
                ],
                [
                    0.0,
                    -1.0,
                    -2.220446049250313e-16
                ],
                [
                    1.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    2.220446049250313e-16,
                    -1.0
                ],
                [
                    0.0,
                    1.0,
                    2.220446049250313e-16
                ],
                [
                    -1.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    -2.220446049250313e-16,
                    1.0
                ],
                [
                    0.0,
                    -1.0,
                    -2.220446049250313e-16
                ],
                [
                    -1.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    2.220446049250313e-16,
                    -1.0
                ],
                [
                    0.0,
                    -1.0,
                    -2.220446049250313e-16
                ]
            ],
            "degree": 1
        }
    ]
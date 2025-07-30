"""
Implement a class to manage a system of layers, where:

Each layer has an ID (like 1, 2, 3)
Each layer contains properties stored as key-value pairs
Example of a layer: Layer(1, {"color": "green"})
Part 1: Basic Operations
Implement a class with the following operations:

init()
apply(layer)
undo()
Example Flow:
# Operation 1
apply(Layer(1, {"color": "green"}))

# Operation 2
apply(Layer(2, {"shape": "triangle", "color": "blue"}))

# Operation 3
apply(Layer(1, {"color": "pink"}))

# After these operations, system state is:
# Layer 1: {"color": "pink"}
# Layer 2: {"shape": "triangle", "color": "blue"}

# After one undo(), system state becomes:
# Layer 1: {"color": "green"}
# Layer 2: {"shape": "triangle", "color": "blue"}

# After another undo(), system state becomes:
# Layer 1: {"color": "green"}
Part 2: Batch Operations
Add support for batch operations with these additional features:

commit_batch(): Groups preceding operations into a single batch
Undo should work at batch level
Example Flow with Batches:
# Batch 1
apply(Layer(1, {"color": "green"}))
apply(Layer(2, {"shape": "triangle", "color": "blue"}))
apply(Layer(1, {"color": "pink"}))
commit_batch()

# Batch 2
apply(Layer(1, {"color": "blue"}))
apply(Layer(1, {"color": "white"}))
commit_batch()

# Final state after both batches:
# Layer 1: {"color": "white"}
# Layer 2: {"shape": "triangle", "color": "blue"}

# After one undo() (reverting Batch 2):
# Layer 1: {"color": "pink"}
# Layer 2: {"shape": "triangle", "color": "blue"}
Part 3: Redo Functionality
Add redo capability:

New method: redo()
Restores previously undone operations


not going to worry about layer ordering at first - probably best to have a sort key of some sort

undo stack: keep track of the opposite action

actions in apply -> undo action
- create new layer -> delete layer
- add property -> remove property
- change property from A to B -> change property from B to A
"""

from typing import Dict
import unittest


class Layers:
    def __init__(self):
        self.layers = {}
        self.undo_stack = []

    def apply(self, layer_id: str, props: Dict):
        if layer_id not in self.layers:
            self.undo_stack.append(("DELETE_LAYER", layer_id))
            self.layers[layer_id] = props
            return
    def apply(self, layer_id: str, props: Dict):
        if layer_id not in self.layers:
            # New layer: undo is to delete the layer
            self.undo_stack.append(("DELETE_LAYER", layer_id))
            self.layers[layer_id] = props.copy()
            return

        # Existing layer: we want to record the previous values of all keys in props
        prev_props = {
            k: self.layers[layer_id][k] if k in self.layers[layer_id] else None for k in props
        }

        self.undo_stack.append(("SET_PROPS", layer_id, prev_props))

        # Apply all changes
        for k, v in props.items():
            self.layers[layer_id][k] = v


    def undo(self):
        if not self.undo_stack:
            return  # Nothing to undo

        action = self.undo_stack.pop()
        if action[0] == "DELETE_LAYER":
            # Undo a layer creation: delete the layer
            layer_id = action[1]
            if layer_id in self.layers:
                del self.layers[layer_id]
        elif action[0] == "SET_PROPS":
            # Undo a property set: restore previous values
            layer_id = action[1]
            prev_props = action[2]
            if layer_id in self.layers:
                for k, v in prev_props.items():
                    if v is None:
                        # Property didn't exist before, so remove it
                        if k in self.layers[layer_id]:
                            del self.layers[layer_id][k]
                    else:
                        self.layers[layer_id][k] = v


                        # INSERT_YOUR_CODE
import unittest

class TestLayerSystem(unittest.TestCase):
    def setUp(self):
        self.LayerSystem = Layers

    def test_apply_new_layer(self):
        ls = self.LayerSystem()
        ls.apply("layer1", {"opacity": 0.5, "visible": True})
        self.assertIn("layer1", ls.layers)
        self.assertEqual(ls.layers["layer1"], {"opacity": 0.5, "visible": True})
        self.assertEqual(ls.undo_stack[-1], ("DELETE_LAYER", "layer1"))

    def test_apply_existing_layer(self):
        ls = self.LayerSystem()
        ls.layers["layer1"] = {"opacity": 0.5, "visible": True}
        ls.apply("layer1", {"opacity": 0.8})
        self.assertEqual(ls.layers["layer1"]["opacity"], 0.8)
        self.assertEqual(ls.layers["layer1"]["visible"], True)
        self.assertEqual(ls.undo_stack[-1][0], "SET_PROPS")
        self.assertEqual(ls.undo_stack[-1][1], "layer1")
        self.assertEqual(ls.undo_stack[-1][2], {"opacity": 0.5})

    def test_undo_delete_layer(self):
        ls = self.LayerSystem()
        ls.apply("layer1", {"opacity": 0.5})
        self.assertIn("layer1", ls.layers)
        ls.undo()
        self.assertNotIn("layer1", ls.layers)

    def test_undo_set_props(self):
        ls = self.LayerSystem()
        ls.layers["layer1"] = {"opacity": 0.5, "visible": True}
        ls.apply("layer1", {"opacity": 0.8, "color": "red"})
        self.assertEqual(ls.layers["layer1"]["opacity"], 0.8)
        self.assertEqual(ls.layers["layer1"]["color"], "red")
        ls.undo()
        self.assertEqual(ls.layers["layer1"]["opacity"], 0.5)
        self.assertNotIn("color", ls.layers["layer1"])
        self.assertEqual(ls.layers["layer1"]["visible"], True)

    def test_undo_nothing(self):
        ls = self.LayerSystem()
        # Should not raise
        ls.undo()
        self.assertEqual(ls.layers, {})

    def test_multiple_undos(self):
        ls = self.LayerSystem()
        ls.apply("layer1", {"opacity": 0.5})
        ls.apply("layer1", {"opacity": 0.8})
        ls.apply("layer1", {"visible": False})
        self.assertEqual(ls.layers["layer1"], {"opacity": 0.8, "visible": False})
        ls.undo()
        self.assertNotIn("visible", ls.layers["layer1"])
        self.assertEqual(ls.layers["layer1"]["opacity"], 0.8)
        ls.undo()
        self.assertEqual(ls.layers["layer1"]["opacity"], 0.5)
        ls.undo()
        self.assertNotIn("layer1", ls.layers)

if __name__ == "__main__":
    unittest.main()


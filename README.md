# Realize No Modifiers

Blender add-on to do **Make Instances Real** without copying all modifiers to each object, this avoids out of memory crashes and removes the step of clearing modifiers. You will still need to manually add back modifiers (eg Solidify) before the instancer (geometry nodes) though which can be done quickly using **Copy to Selected** or **Copy Modifiers**, just make sure you don't accidentally add the instancer too.

You can find the new **Make Instances Real (no modifiers)** under **Object > Apply**, the same place the original one is.

Tested on Blender 4.1.1
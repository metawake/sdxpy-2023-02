import math

# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

def make(cls, *args):
    """Make an 'instance' of a 'class'."""
    return cls["_new"](*args)

def find(thing, method_name):
    """Find a method."""
    if thing is None:
        raise NotImplementedError("method_name")
    if method_name in thing:
        return thing[method_name]
    cls = thing.get("_class", None)
    if cls is None:
        #raise NotImplementedError(method_name)
        return None
    if method_name in cls:
        return cls[method_name]
    parents = [cls["_parent"]] if type(cls["_parent"]) is dict else cls["_parent"]
    for parent in parents:
        method = find(parent, method_name)
        if method:
            return method
    raise NotImplementedError("method_name not found in neither parents")

def call(thing, method_name, *args):
    """Call a method."""
    method = find(thing, method_name)
    if not callable(method):
        return method
    return method(thing, *args)

# ----------------------------------------------------------------------
# The generic Shape class.
# ----------------------------------------------------------------------

def shape_new(name):
    """Build a generic shape."""
    return {
        "name": name,
        "_class": Shape
    }

def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")

# Properties of the Shape 'class'.
Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new
}

# ----------------------------------------------------------------------
# The Square class (derived from Shape).
# ----------------------------------------------------------------------

def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]

def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2

def square_new(name, side):
    """Construct a square (a Shape with extra/overridden properties)."""
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }

# Properties of the Square 'class'.
Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new
}

# ----------------------------------------------------------------------
# The Square class (derived from Shape).
# ----------------------------------------------------------------------

def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2

def circle_new(name, radius):
    """Construct a circle (a Shape with extra/overridden properties)."""
    return make(Shape, name) | {
        "radius": radius,
        "_class": Circle
    }

# Properties of the Circle 'class'.
Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parent": Shape,
    "_new": circle_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        print(f"{n}: {d:.2f}")
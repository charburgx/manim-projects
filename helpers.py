from manimlib import *

# Nice animation for writing a matrix
def WriteMatrix(matrix, lr=0.1):
    return AnimationGroup(
            Write(matrix.get_entries(), lag_ratio=0), 
            Write(matrix.get_brackets()),
            lag_ratio=lr)

# Rotates an object based on local coordinate of a given coordinate axes
def RotateAxes(obj, axes, angle, to, abt_point=np.array((0, 0, 0)), **kwargs):
    obj.rotate(angle, axes.c2p(*to) - axes.c2p(*abt_point), about_point=axes.c2p(*abt_point), **kwargs)

def ColorInt(col, colorto):
    #color = obj.get_color()
    return lambda m: m.set_fill(
        color=interpolate_color(
            col, colorto, m.get_opacity()), 
            opacity=m.get_opacity())
    #colorto = kwargs["colorto"]
    #color = obj.get_color()
    #anim = Write(obj, **kwargs)

    #colorInt = lambda m: m.set_fill(color=interpolate_color(color, colorto, m.get_opacity()), opacity=m.get_opacity())
    #colorIntOut = lambda m: m.set_fill(color=interpolate_color(color, colorto, (m.get_rate_func())(m.get)), opacity=m.get_opacity())

#obj.add_updater(colorInt)

#return AnimationGroup(
#    anim,
#    #anim.get_outline().animate.set_color(colorto),
#    lag_ratio=0
#)

def transformed(transforms):
    return list(map(lambda anim: anim.mobject, transforms))
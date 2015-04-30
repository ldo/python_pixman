"""A Python 3 wrapper for the Pixman pixel-manipulation library <http://www.pixman.org/>.

Pixman is not well documented. But I have tried to fill in docstrings and comments
where I can, based on looking at the source code and my own experiments.
"""
#+
# Copyright 2015 Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
# Licensed under the GNU Lesser General Public License v2.1 or later.
#-

from numbers import \
    Number
import ctypes as ct
import qahirah as qah
from qahirah import \
    CAIRO

pixman = ct.cdll.LoadLibrary("libpixman-1.so.0")
libc = ct.cdll.LoadLibrary("libc.so.6")

class PIXMAN :
    "useful definitions adapted from pixman-1/pixman.h. You will need to use the" \
    " constants, but apart from that, see the more Pythonic wrappers defined outside" \
    " this class in preference to accessing low-level structures directly."

    # General ctypes gotcha: when passing addresses of ctypes-constructed objects
    # to routine calls, do not construct the objects directly in the call. Otherwise
    # the refcount goes to 0 before the routine is actually entered, and the object
    # can get prematurely disposed. Always store the object reference into a local
    # variable, and pass the value of the variable instead.

    fixed_32_32_t = ct.c_long
    fixed_48_16_t = ct.c_long
    fixed_1_31_t = ct.c_uint
    fixed_1_16_t = ct.c_uint
    fixed_16_16_t = ct.c_int
    fixed_t = fixed_16_16_t
    fixed_t_ptr = ct.POINTER(fixed_t)

    fixed_to_int = lambda f : round(f / 65536)
    int_to_fixed = lambda i : i * 65536
    fixed_to_double = lambda f : f / 65536
    double_to_fixed = lambda f : round(f * 65536)
    fixed_e = 1 # closest nonzero value to zero
    fixed_1 = 1 << 16
    fixed_1_minus_e = fixed_1 - fixed_e
    fixed_minus_1 = - fixed_1
    fixed_frac = lambda f : f & fixed_1_minus_e
    fixed_floor = lambda f : f & ~fixed_1_minus_e
    fixed_ceil = lambda f : fixed_floor(f + fixed_1_minus_e)
    fixed_fraction = fixed_frac
    fixed_mod_2 = lambda f : f & (fixed_1 | fixed_1_minus_e)
    max_fixed_48_16 = 0x7fffffff # huh?
    min_fixed_48_16 = - max_fixed_48_16 - 1

    class color_t(ct.Structure) :
        _fields_ = \
            [
                ("red", ct.c_ushort),
                ("green", ct.c_ushort),
                ("blue", ct.c_ushort),
                ("alpha", ct.c_ushort),
            ]
    #end color_t
    color_t_ptr = ct.POINTER(color_t)

    class point_fixed_t(ct.Structure) :
        pass
    point_fixed_t._fields_ = \
        [
            ("x", fixed_t),
            ("y", fixed_t),
        ]
    #end point_fixed_t

    class line_fixed_t(ct.Structure) :
        pass
    line_fixed_t._fields_ = \
        [
            ("p1", point_fixed_t),
            ("p2", point_fixed_t),
        ]
    #end line_fixed_t

    class vector(ct.Structure) :
        pass
    vector._fields_ = \
        [
            ("vector", fixed_t * 3),
        ]
    #end vector

    class transform(ct.Structure) :
        pass
    transform._fields_ = \
        [
            ("matrix", fixed_t * 3 * 3),
        ]
    #end transform

    class f_vector(ct.Structure) :
        pass
    f_vector._fields_ = \
        [
            ("vector", ct.c_double * 3),
        ]
    #end f_vector

    class f_transform(ct.Structure) :
        pass
    f_transform._fields_ = \
        [
            ("matrix", ct.c_double * 3 * 3),
        ]
    #end f_transform

    repeat_t = ct.c_uint
    # values for repeat_t:
    REPEAT_NONE = 0
    REPEAT_NORMAL = 1
    REPEAT_PAD = 2
    REPEAT_REFLECT = 3

    filter_t = ct.c_uint
    # values for filter_t:
    FILTER_FAST = 0
    FILTER_GOOD = 1
    FILTER_BEST = 2
    FILTER_NEAREST = 3
    FILTER_BILINEAR = 4
    FILTER_CONVOLUTION = 5
    FILTER_SEPARABLE_CONVOLUTION = 6

    op_t = ct.c_uint
    # values for op_t:
    OP_CLEAR = 0x00
    OP_SRC = 0x01
    OP_DST = 0x02
    OP_OVER = 0x03
    OP_OVER_REVERSE = 0x04
    OP_IN = 0x05
    OP_IN_REVERSE = 0x06
    OP_OUT = 0x07
    OP_OUT_REVERSE = 0x08
    OP_ATOP = 0x09
    OP_ATOP_REVERSE = 0x0a
    OP_XOR = 0x0b
    OP_ADD = 0x0c
    OP_SATURATE = 0x0d
    OP_DISJOINT_CLEAR = 0x10
    OP_DISJOINT_SRC = 0x11
    OP_DISJOINT_DST = 0x12
    OP_DISJOINT_OVER = 0x13
    OP_DISJOINT_OVER_REVERSE = 0x14
    OP_DISJOINT_IN = 0x15
    OP_DISJOINT_IN_REVERSE = 0x16
    OP_DISJOINT_OUT = 0x17
    OP_DISJOINT_OUT_REVERSE = 0x18
    OP_DISJOINT_ATOP = 0x19
    OP_DISJOINT_ATOP_REVERSE = 0x1a
    OP_DISJOINT_XOR = 0x1b

    OP_CONJOINT_CLEAR = 0x20
    OP_CONJOINT_SRC = 0x21
    OP_CONJOINT_DST = 0x22
    OP_CONJOINT_OVER = 0x23
    OP_CONJOINT_OVER_REVERSE = 0x24
    OP_CONJOINT_IN = 0x25
    OP_CONJOINT_IN_REVERSE = 0x26
    OP_CONJOINT_OUT = 0x27
    OP_CONJOINT_OUT_REVERSE = 0x28
    OP_CONJOINT_ATOP = 0x29
    OP_CONJOINT_ATOP_REVERSE = 0x2a
    OP_CONJOINT_XOR = 0x2b

    OP_MULTIPLY = 0x30
    OP_SCREEN = 0x31
    OP_OVERLAY = 0x32
    OP_DARKEN = 0x33
    OP_LIGHTEN = 0x34
    OP_COLOUR_DODGE = 0x35
    OP_COLOR_DODGE = 0x35
    OP_COLOUR_BURN = 0x36
    OP_COLOR_BURN = 0x36
    OP_HARD_LIGHT = 0x37
    OP_SOFT_LIGHT = 0x38
    OP_DIFFERENCE = 0x39
    OP_EXCLUSION = 0x3a
    OP_HSL_HUE = 0x3b
    OP_HSL_SATURATION = 0x3c
    OP_HSL_COLOUR = 0x3d
    OP_HSL_COLOR = 0x3d
    OP_HSL_LUMINOSITY = 0x3e

    region_overlap_t = ct.c_uint
    # values for region_overlap_t:
    REGION_OUT = 0
    REGION_IN = 1
    REGION_PART = 2

    class region16_data_t(ct.Structure) :
        _fields_ = \
            [
                ("size", ct.c_long),
                ("numRects", ct.c_long),
              # ("rects", box16_t * size),
            ]
    #end region16_data_t
    region16_data_t_ptr = ct.POINTER(region16_data_t)

    class rectangle16_t(ct.Structure) :
        _fields_ = \
            [
                ("x", ct.c_short),
                ("y", ct.c_short),
                ("width", ct.c_ushort),
                ("height", ct.c_ushort),
            ]
    #end rectangle16_t

    class box16_t(ct.Structure) :
        _fields_ = \
            [
                ("x1", ct.c_short),
                ("y1", ct.c_short),
                ("x2", ct.c_short),
                ("y2", ct.c_short),
            ]
    #end box16_t
    box16_t_ptr = ct.POINTER(box16_t)

    class region16_t(ct.Structure) :
        pass
    region16_t._fields_ = \
        [
            ("extents", box16_t),
            ("data", region16_data_t_ptr),
        ]
    #end region16_t

    class region32_data_t(ct.Structure) :
        _fields_ = \
            [
                ("size", ct.c_long),
                ("numRects", ct.c_long),
              # ("rects", box32_t * size),
            ]
    #end region32_data_t
    region32_data_t_ptr = ct.POINTER(region32_data_t)

    class rectangle32_t(ct.Structure) :
        _fields_ = \
            [
                ("x", ct.c_int),
                ("y", ct.c_int),
                ("width", ct.c_int),
                ("height", ct.c_int),
            ]
    #end rectangle32_t

    class box32_t(ct.Structure) :
        _fields_ = \
            [
                ("x1", ct.c_int),
                ("y1", ct.c_int),
                ("x2", ct.c_int),
                ("y2", ct.c_int),
            ]
    #end box32_t
    box32_t_ptr = ct.POINTER(box32_t)

    class region32_t(ct.Structure) :
        pass
    region32_t._fields_ = \
        [
            ("extents", box32_t),
            ("data", region32_data_t_ptr),
        ]
    #end region32_t

    # Images

    MAX_INDEXED = 256
    index_type = ct.c_uint

    class indexed_t(ct.Structure) :
        pass
    indexed_t._fields_ = \
        [
            ("color", ct.c_bool),
            ("rgba", ct.c_uint * MAX_INDEXED),
            ("ent", index_type * 32768),
        ]
    #end indexed_t

    class gradient_stop_t(ct.Structure) :
        pass
    gradient_stop_t._fields_ = \
        [
            ("x", fixed_t),
            ("color", color_t),
        ]
    #end gradient_stop_t

    read_memory_func_t = ct.CFUNCTYPE(ct.c_uint, ct.c_void_p, ct.c_int)
    write_memory_func_t = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_uint, ct.c_int)
    image_destroy_func_t = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_void_p)

    def FORMAT(bpp, type, a, r, g, b) :
        "generates a Pixman format code from the specified components."
        return \
            (
                bpp << 24
            |
                type << 16
            |
                a << 12
            |
                r << 8
            |
                g << 4
            |
                b
            )
    #end FORMAT

    FORMAT_BPP = lambda f : f >> 24
    FORMAT_TYPE = lambda f : f >> 16 & 0xff
    FORMAT_A = lambda f : f >> 12 & 0x0f
    FORMAT_R = lambda f : f >> 8 & 0x0f
    FORMAT_G = lambda f : f >> 4 & 0x0f
    FORMAT_B = lambda f : f & 0x0f
    FORMAT_RGB = lambda f : f & 0xfff
    FORMAT_VIS = lambda f : f & 0xffff
    FORMAT_DEPTH = lambda f : FORMAT_A(f) + FORMAT_R(f) + FORMAT_G(f) + FORMAT_B(f)

    TYPE_OTHER = 0
    TYPE_A = 1
    TYPE_ARGB = 2
    TYPE_ABGR = 3
    TYPE_COLOUR = 4
    TYPE_COLOR = 4
    TYPE_GRAY = 5
    TYPE_YUY2 = 6
    TYPE_YV12 = 7
    TYPE_BGRA = 8
    TYPE_RGBA = 9
    TYPE_ARGB_SRGB = 10

    FORMAT_COLOUR = lambda f : FORMAT_TYPE(f) in (TYPE_ARGB, TYPE_ABGR, TYPE_BGRA, TYPE_RGBA)
    FORMAT_COLOR = FORMAT_COLOUR

    format_code_t = ct.c_uint
    # values for format_code_t -- 32 bits per pixel
    a8r8g8b8 = FORMAT(32,TYPE_ARGB,8,8,8,8)
    x8r8g8b8 = FORMAT(32,TYPE_ARGB,0,8,8,8)
    a8b8g8r8 = FORMAT(32,TYPE_ABGR,8,8,8,8)
    x8b8g8r8 = FORMAT(32,TYPE_ABGR,0,8,8,8)
    b8g8r8a8 = FORMAT(32,TYPE_BGRA,8,8,8,8)
    b8g8r8x8 = FORMAT(32,TYPE_BGRA,0,8,8,8)
    r8g8b8a8 = FORMAT(32,TYPE_RGBA,8,8,8,8)
    r8g8b8x8 = FORMAT(32,TYPE_RGBA,0,8,8,8)
    x14r6g6b6 = FORMAT(32,TYPE_ARGB,0,6,6,6)
    x2r10g10b10 = FORMAT(32,TYPE_ARGB,0,10,10,10)
    a2r10g10b10 = FORMAT(32,TYPE_ARGB,2,10,10,10)
    x2b10g10r10 = FORMAT(32,TYPE_ABGR,0,10,10,10)
    a2b10g10r10 = FORMAT(32,TYPE_ABGR,2,10,10,10)

    # sRGB
    a8r8g8b8_sRGB = FORMAT(32,TYPE_ARGB_SRGB,8,8,8,8)

    # values for format_code_t -- 24 bits per pixel
    r8g8b8 = FORMAT(24,TYPE_ARGB,0,8,8,8)
    b8g8r8 = FORMAT(24,TYPE_ABGR,0,8,8,8)

    # values for format_code_t -- 16 bits per pixel
    r5g6b5 = FORMAT(16,TYPE_ARGB,0,5,6,5)
    b5g6r5 = FORMAT(16,TYPE_ABGR,0,5,6,5)

    a1r5g5b5 = FORMAT(16,TYPE_ARGB,1,5,5,5)
    x1r5g5b5 = FORMAT(16,TYPE_ARGB,0,5,5,5)
    a1b5g5r5 = FORMAT(16,TYPE_ABGR,1,5,5,5)
    x1b5g5r5 = FORMAT(16,TYPE_ABGR,0,5,5,5)
    a4r4g4b4 = FORMAT(16,TYPE_ARGB,4,4,4,4)
    x4r4g4b4 = FORMAT(16,TYPE_ARGB,0,4,4,4)
    a4b4g4r4 = FORMAT(16,TYPE_ABGR,4,4,4,4)
    x4b4g4r4 = FORMAT(16,TYPE_ABGR,0,4,4,4)

    # values for format_code_t -- 8 bits per pixel
    a8 = FORMAT(8,TYPE_A,8,0,0,0)
    r3g3b2 = FORMAT(8,TYPE_ARGB,0,3,3,2)
    b2g3r3 = FORMAT(8,TYPE_ABGR,0,3,3,2)
    a2r2g2b2 = FORMAT(8,TYPE_ARGB,2,2,2,2)
    a2b2g2r2 = FORMAT(8,TYPE_ABGR,2,2,2,2)

    c8 = FORMAT(8,TYPE_COLOUR,0,0,0,0)
    g8 = FORMAT(8,TYPE_GRAY,0,0,0,0)

    x4a4 = FORMAT(8,TYPE_A,4,0,0,0)

    x4c4 = FORMAT(8,TYPE_COLOUR,0,0,0,0)
    x4g4 = FORMAT(8,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- 4 bits per pixel
    a4 = FORMAT(4,TYPE_A,4,0,0,0)
    r1g2b1 = FORMAT(4,TYPE_ARGB,0,1,2,1)
    b1g2r1 = FORMAT(4,TYPE_ABGR,0,1,2,1)
    a1r1g1b1 = FORMAT(4,TYPE_ARGB,1,1,1,1)
    a1b1g1r1 = FORMAT(4,TYPE_ABGR,1,1,1,1)

    c4 = FORMAT(4,TYPE_COLOUR,0,0,0,0)
    g4 = FORMAT(4,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- 1 bit per pixel
    a1 = FORMAT(1,TYPE_A,1,0,0,0)

    g1 = FORMAT(1,TYPE_GRAY,0,0,0,0)

    # values for format_code_t -- YUV
    yuy2 = FORMAT(16,TYPE_YUY2,0,0,0,0)
    yv12 = FORMAT(12,TYPE_YV12,0,0,0,0)

    kernel_t = ct.c_uint
    # values for kernel_t:
    KERNEL_IMPULSE = 0
    KERNEL_BOX = 1
    KERNEL_LINEAR = 2
    KERNEL_CUBIC = 3
    KERNEL_GAUSSIAN = 4
    KERNEL_LANCZOS2 = 5
    KERNEL_LANCZOS3 = 6
    KERNEL_LANCZOS3_STRETCHED = 7

    # TODO: glyphs

#end PIXMAN

all_format_names = frozenset \
    (( # all names of Pixman pixel formats
        "a8r8g8b8",
        "x8r8g8b8",
        "a8b8g8r8",
        "x8b8g8r8",
        "b8g8r8a8",
        "b8g8r8x8",
        "r8g8b8a8",
        "r8g8b8x8",
        "x14r6g6b6",
        "x2r10g10b10",
        "a2r10g10b10",
        "x2b10g10r10",
        "a2b10g10r10",
        # sRGB
        "a8r8g8b8_sRGB",
        # values for format_code_t -- 24 bits per pixel
        "r8g8b8",
        "b8g8r8",
        # values for format_code_t -- 16 bits per pixel
        "r5g6b5",
        "b5g6r5",
        "a1r5g5b5",
        "x1r5g5b5",
        "a1b5g5r5",
        "x1b5g5r5",
        "a4r4g4b4",
        "x4r4g4b4",
        "a4b4g4r4",
        "x4b4g4r4",
        # values for format_code_t -- 8 bits per pixel
        "a8",
        "r3g3b2",
        "b2g3r3",
        "a2r2g2b2",
        "a2b2g2r2",
        "c8",
        "g8",
        "x4a4",
        "x4c4",
        "x4g4",
        # values for format_code_t -- 4 bits per pixel
        "a4",
        "r1g2b1",
        "b1g2r1",
        "a1r1g1b1",
        "a1b1g1r1",
        "c4",
        "g4",
        # values for format_code_t -- 1 bit per pixel
        "a1",
        "g1",
        # values for format_code_t -- YUV
        "yuy2",
        "yv12",
    ))
cairo_to_pixman_format = \
    { # Pixman pixel formats corresponding to Cairo pixel formats
        CAIRO.FORMAT_ARGB32 : PIXMAN.a8r8g8b8,
        CAIRO.FORMAT_RGB24 : PIXMAN.x8r8g8b8,
        CAIRO.FORMAT_A8 : PIXMAN.a8,
        CAIRO.FORMAT_A1 : PIXMAN.a1,
        CAIRO.FORMAT_RGB16_565 : PIXMAN.r5g6b5,
        CAIRO.FORMAT_RGB30 : PIXMAN.x2r10g10b10,
    }
pixman_to_cairo_format = dict((cairo_to_pixman_format[k], k) for k in cairo_to_pixman_format)
  # and mapping back the other way

# TODO: fixed-point and floating-point transformations
# Note there is only the minimum of 16-bit region support
pixman.pixman_region_init.restype = None
pixman.pixman_region_init.argtypes = (ct.c_void_p,)
pixman.pixman_region_fini.restype = None
pixman.pixman_region_fini.argtypes = (ct.c_void_p,)
pixman.pixman_region_rectangles.restype = ct.c_void_p
pixman.pixman_region_rectangles.argtypes = (ct.c_void_p, ct.c_void_p)

pixman.pixman_region32_init.restype = None
pixman.pixman_region32_init.argtypes = (ct.c_void_p,)
pixman.pixman_region32_init_rect.restype = None
pixman.pixman_region32_init_rect.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_init_rects.restype = ct.c_bool
pixman.pixman_region32_init_rects.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int)
pixman.pixman_region32_init_with_extents.restype = None
pixman.pixman_region32_init_with_extents.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_init_from_image.restype = None
pixman.pixman_region32_init_from_image.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_fini.restype = None
pixman.pixman_region32_fini.argtypes = (ct.c_void_p,)
pixman.pixman_region32_translate.restype = None
pixman.pixman_region32_translate.argtypes = (ct.c_void_p, ct.c_int, ct.c_int)
pixman.pixman_region32_copy.restype = ct.c_bool
pixman.pixman_region32_copy.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_intersect.restype = ct.c_bool
pixman.pixman_region32_intersect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_union.restype = ct.c_bool
pixman.pixman_region32_union.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_intersect_rect.restype = ct.c_bool
pixman.pixman_region32_intersect_rect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_union_rect.restype = ct.c_bool
pixman.pixman_region32_union_rect.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint, ct.c_uint)
pixman.pixman_region32_subtract.restype = ct.c_bool
pixman.pixman_region32_subtract.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_inverse.restype = ct.c_bool
pixman.pixman_region32_inverse.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_contains_point.restype = ct.c_bool
pixman.pixman_region32_contains_point.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p)
pixman.pixman_region32_contains_rectangle.restype = PIXMAN.region_overlap_t
pixman.pixman_region32_contains_rectangle.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_not_empty.restype = ct.c_bool
pixman.pixman_region32_not_empty.argtypes = (ct.c_void_p,)
pixman.pixman_region32_extents.restype = PIXMAN.box32_t_ptr
pixman.pixman_region32_extents.argtypes = (ct.c_void_p,)
pixman.pixman_region32_n_rects.restype = ct.c_int
pixman.pixman_region32_n_rects.argtypes = (ct.c_void_p,)
pixman.pixman_region32_rectangles.restype = ct.c_void_p
pixman.pixman_region32_rectangles.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_equal.restype = ct.c_bool
pixman.pixman_region32_equal.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_selfcheck.restype = ct.c_bool
pixman.pixman_region32_selfcheck.argtypes = (ct.c_void_p,)
pixman.pixman_region32_reset.restype = None
pixman.pixman_region32_reset.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_region32_clear.restype = None
pixman.pixman_region32_clear.argtypes = (ct.c_void_p,)

pixman.pixman_blt.restype = ct.c_bool
pixman.pixman_blt.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int)
pixman.pixman_fill.restype = ct.c_bool
pixman.pixman_fill.argtypes = (ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_uint)
pixman.pixman_version.restype = ct.c_int
pixman.pixman_version_string.restype = ct.c_char_p

pixman.pixman_format_supported_destination.restype = ct.c_bool
pixman.pixman_format_supported_destination.argtypes = (ct.c_uint,)
pixman.pixman_format_supported_source.restype = ct.c_bool
pixman.pixman_format_supported_source.argtypes = (ct.c_uint,)

pixman.pixman_image_create_solid_fill.restype = ct.c_void_p
pixman.pixman_image_create_solid_fill.argtypes = (ct.c_void_p,)
pixman.pixman_image_create_linear_gradient.restype = ct.c_void_p
pixman.pixman_image_create_linear_gradient.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_radial_gradient.restype = ct.c_void_p
pixman.pixman_image_create_radial_gradient.argtypes = (ct.c_void_p, ct.c_void_p, PIXMAN.fixed_t, PIXMAN.fixed_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_conical_gradient.restype = ct.c_void_p
pixman.pixman_image_create_conical_gradient.argtypes = (ct.c_void_p, PIXMAN.fixed_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_bits.restype = ct.c_void_p
pixman.pixman_image_create_bits.argtypes = (PIXMAN.format_code_t, ct.c_int, ct.c_int, ct.c_void_p, ct.c_int)
pixman.pixman_image_create_bits_no_clear.restype = ct.c_void_p
pixman.pixman_image_create_bits_no_clear.argtypes = (PIXMAN.format_code_t, ct.c_int, ct.c_int, ct.c_void_p, ct.c_int)
pixman.pixman_image_ref.restype = ct.c_void_p
pixman.pixman_image_ref.argtypes = (ct.c_void_p,)
pixman.pixman_image_unref.restype = ct.c_bool
pixman.pixman_image_unref.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_destroy_function.restype = None
pixman.pixman_image_set_destroy_function.argtypes = (ct.c_void_p, PIXMAN.image_destroy_func_t, ct.c_void_p)
pixman.pixman_image_get_destroy_data.restype = ct.c_void_p # not used
pixman.pixman_image_get_destroy_data.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_clip_region32.restype = ct.c_bool
pixman.pixman_image_set_clip_region32.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_set_has_client_clip.restype = None
pixman.pixman_image_set_has_client_clip.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_set_transform.restype = ct.c_bool
pixman.pixman_image_set_transform.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_set_repeat.restype = None
pixman.pixman_image_set_repeat.argtypes = (ct.c_void_p, PIXMAN.repeat_t)
pixman.pixman_image_set_filter.restype = ct.c_bool
pixman.pixman_image_set_filter.argtypes = (ct.c_void_p, PIXMAN.filter_t, ct.c_void_p, ct.c_int)
pixman.pixman_image_set_source_clipping.restype = None
pixman.pixman_image_set_source_clipping.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_set_alpha_map.restype = None
pixman.pixman_image_set_alpha_map.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short)
pixman.pixman_image_set_component_alpha.restype = None
pixman.pixman_image_set_component_alpha.argtypes = (ct.c_void_p, ct.c_bool)
pixman.pixman_image_get_component_alpha.restype = ct.c_bool
pixman.pixman_image_get_component_alpha.argtypes = (ct.c_void_p,)
pixman.pixman_image_set_accessors.restype = None
pixman.pixman_image_set_accessors.argtypes = (ct.c_void_p, PIXMAN.read_memory_func_t, PIXMAN.write_memory_func_t)
pixman.pixman_image_set_indexed.restype = None
pixman.pixman_image_set_indexed.argtypes = (ct.c_void_p, ct.c_void_p)
pixman.pixman_image_get_data.restype = ct.c_void_p
pixman.pixman_image_get_data.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_width.restype = ct.c_int
pixman.pixman_image_get_width.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_height.restype = ct.c_int
pixman.pixman_image_get_height.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_stride.restype = ct.c_int
pixman.pixman_image_get_stride.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_depth.restype = ct.c_int
pixman.pixman_image_get_depth.argtypes = (ct.c_void_p,)
pixman.pixman_image_get_format.restype = PIXMAN.format_code_t
pixman.pixman_image_get_format.argtypes = (ct.c_void_p,)
pixman.pixman_filter_create_separable_convolution.restype = ct.c_void_p
pixman.pixman_filter_create_separable_convolution.argtypes = (ct.c_void_p, PIXMAN.fixed_t, PIXMAN.fixed_t, PIXMAN.kernel_t, PIXMAN.kernel_t, PIXMAN.kernel_t, PIXMAN.kernel_t, ct.c_int, ct.c_int)
pixman.pixman_image_fill_rectangles.restype = ct.c_bool # not used
pixman.pixman_image_fill_rectangles.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p)
pixman.pixman_image_fill_boxes.restype = ct.c_bool
pixman.pixman_image_fill_boxes.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_void_p)
pixman.pixman_compute_composite_region.restype = ct.c_bool
pixman.pixman_compute_composite_region.argtypes = (ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short)
pixman.pixman_image_composite.restype = None # not used
pixman.pixman_image_composite.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short, ct.c_short)
pixman.pixman_image_composite32.restype = None
pixman.pixman_image_composite32.argtypes = (PIXMAN.op_t, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_int)

# TODO: glyphs

libc.malloc.restype = ct.c_void_p
libc.malloc.argtypes = (ct.c_size_t,)
libc.free.restype = None
libc.free.argtypes = (ct.c_void_p,)

#+
# Higher-level stuff follows
#-

def version() :
    "returns the integer Pixman version."
    return \
        pixman.pixman_version()
#end version

def version_string() :
    "returns the Pixman version string."
    return \
        pixman.pixman_version_string()
#end version_string

class Point(qah.Vector) :
    "augment qahirah.Vector with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    def isshortint(self) :
        "are the components signed 16-bit integers."
        return \
            qah.int_fits_bits(self.x, 16) and qah.int_fits_bits(self.y, 16)
    #end isshortint

    def assert_isshortint(self) :
        "checks that the components are signed 16-bit integers."
        if not self.isshortint() :
            raise ValueError("components must be signed 16-bit integers")
        #end if
        return \
            self
    #end assert_isshortint

    @classmethod
    def from_pixman_fixed(celf, p) :
        return \
            celf \
              (
                x = PIXMAN.fixed_t_double(p.x),
                y = PIXMAN.fixed_t_double(p.y),
              )
    #end from_pixman_fixed

    def to_pixman_fixed(self) :
        return \
            PIXMAN.point_fixed_t \
              (
                x = PIXMAN.double_to_fixed(self.x),
                y = PIXMAN.double_to_fixed(self.y),
              )
    #end to_pixman_fixed

#end Point

class Rect(qah.Rect) :
    "augment qahirah.Rect with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    @classmethod
    def from_pixman_box(celf, b) :
        return \
            celf.from_corners((b.x1, b.y1), (b.x2, b.y2))
    #end from_pixman_box

    def isshortint(self) :
        "are the components signed 16-bit integers."
        return \
            (
                qah.int_fits_bits(self.left, 16)
            and
                qah.int_fits_bits(self.top, 16)
            and
                qah.int_fits_bits(self.width, 16)
            and
                qah.int_fits_bits(self.height, 16)
            )
    #end isshortint

    def assert_isshortint(self) :
        "checks that the components are signed 16-bit integers."
        if not self.isshortint() :
            raise ValueError("components must be signed 16-bit integers")
        #end if
        return \
            self
    #end assert_isshortint

    def to_pixman_rect16(self) :
        self.assert_isshortint()
        return \
            PIXMAN.rectangle16_t(self.left, self.top, self.width, self.height)
    #end to_pixman_rect16

    def to_pixman_rect(self) :
        self.assert_isint()
        return \
            PIXMAN.rectangle32_t(self.left, self.top, self.width, self.height)
    #end to_pixman_rect

    def to_pixman_box(self) :
        self.assert_isint()
        return \
            PIXMAN.box32_t(self.left, self.top, self.right, self.bottom)
    #end to_pixman_box

#end Rect

class Region :
    "wrapper for a Pixman region32_t. Do not instantiate directly; use one of the create" \
    " methods.\n" \
    "\n" \
    "A Region is a collection of integer pixel coordinates with arbitrary connectivity (i.e." \
    " it can consist of multiple discontiguous pieces with holes). It is represented as a" \
    " sequence of rectangles, such that all coordinates within each rectangle are part of" \
    " the Region."

    __slots__ = ("_region",) # to forestall typos

    def __init__(self) :
        self._region = PIXMAN.region32_t() # structure must be initialized by caller
    #end __init__

    @staticmethod
    def create() :
        result = Region()
        pixman.pixman_region32_init(ct.byref(result._region))
        return \
            result
    #end create

    @staticmethod
    def create_rect(rect) :
        result = Region()
        rect.assert_isint()
        pixman.pixman_region32_init_rect(ct.byref(result._region), rect.left, rect.top, rect.width, rect.height)
        return \
            result
    #end create_rect

    @staticmethod
    def create_rects(rects) :
        result = Region()
        nr_rects = len(rects)
        c_rects = (PIXMAN.box32_t * nr_rects)()
        for i in range(nr_rects) :
            rects[i].assert_isint()
            c_rects[i] = rects[i].to_pixman_box()
        #end for
        validated = pixman.pixman_region32_init_rects(ct.byref(result._region), ct.byref(c_rects), nr_rects)
        return \
            (result, validated)
    #end create_rects

    @staticmethod
    def create_with_extents(extents) :
        result = Region()
        extents.assert_isint()
        c_extents = extents.to_pixman_box()
        pixman.pixman_region32_init_with_extents(ct.byref(result._region), ct.byref(c_extents))
        return \
            result
    #end create_with_extents

    @staticmethod
    def create_from_image(image) :
        if not isinstance(image, Image) :
            raise TypeError("image must be an Image")
        #end if
        result = Region()
        pixman.pixman_region32_init_from_image(ct.byref(result._region), image._pmobj)
        return \
            result
    #end create_from_image

    def __del__(self) :
        if self._region != None :
            pixman.pixman_region32_fini(ct.byref(self._region))
            self._region = None
        #end if
    #end __del__

    def translate(offset) :
        offset = Point.from_tuple(offset).assert_isint()
        pixman.pixman_region32_translate(ct.byref(self._region), offset.x, offset.y)
        return \
            self
    #end translate

    def copy(self, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        if not pixman.pixman_region32_copy(ct.byref(dest._region), ct.byref(self._region)) :
            raise MemoryError("Pixman couldn’t copy region")
        #end if
        return \
            self
    #end copy

    def intersect(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_intersect(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t intersect regions")
        #end if
        return \
            self
    #end intersect

    def union(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_union(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t union regions")
        #end if
        return \
            self
    #end intersect

    def intersect_rect(self, rect, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        rect.assert_isint()
        if not pixman.pixman_region32_intersect_rect(ct.byref(dest._region), ct.byref(self._region), rect.left, rect.top, rect.width, rect.height) :
            raise MemoryError("Pixman couldn’t intersect region")
        #end if
        return \
            self
    #end intersect_rect

    def union_rect(self, rect, dest) :
        if not isinstance(dest, Region) :
            raise TypeError("dest must be a Region")
        #end if
        rect.assert_isint()
        if not pixman.pixman_region32_union_rect(ct.byref(dest._region), ct.byref(self._region), rect.left, rect.top, rect.width, rect.height) :
            raise MemoryError("Pixman couldn’t union region")
        #end if
        return \
            self
    #end union_rect

    def subtract(reg1, reg2, new_reg) :
        if not isinstance(reg1, Region) or not isinstance(new_reg, Region) :
            raise TypeError("args must be Regions")
        #end if
        if not pixman.pixman_region32_subtract(ct.byref(new_reg._region), ct.byref(reg1._region), ct.byref(reg2._region)) :
            raise MemoryError("Pixman couldn’t subtract regions")
        #end if
        return \
            self
    #end subtract

    def inverse(self, inv_rect, new_reg) :
        if not isinstance(new_reg, Region) :
            raise TypeError("new_reg must be Region")
        #end if
        inv_rect.assert_isint()
        c_inv_rect = inv_rect.to_pixman_box()
        if not pixman.pixman_region32_inverse(ct.byref(self._region), ct.byref(c_inv_rect), ct.byref(new_reg._region)) :
            raise MemoryError("Pixman couldn’t invert region")
        #end if
        return \
            self
    #end inverse

    def contains_point(self, point, want_box = False) :
        point = Point.from_tuple(point).assert_isint()
        if want_box :
            box = ct.pointer(PIXMAN.box32_t())
        else :
            box = None
        #end if
        contains = pixman.pixman_region32_contains_point(ct.byref(self._region), point.x, point.y, box)
        if want_box :
            result = (contains, Rect.from_pixman_box(box.contents))
        else :
            result = contains
        #end if
        return \
            result
    #end contains_point

    def contains_rectangle(self, prect) :
        c_prect = prect.to_pixman_box()
        return \
            pixman.pixman_region32_contains_rectangle(ct.byref(self._region), ct.byref(c_prect))
    #end contains_rectangle

    @property
    def not_empty(self) :
        return \
            pixman.pixman_region32_not_empty(ct.byref(self._region))
    #end not_empty

    @property
    def extents(self) :
        return \
            Rect.from_pixman_box(pixman.pixman_region32_extents(ct.byref(self._region)).contents)
    #end extents

    @property
    def n_rects(self) :
        "the number of rectangles making up the Region."
        return \
            pixman.pixman_region32_n_rects(ct.byref(self._region))
    #end n_rects

    def rectangles(self) :
        "iterates over the rectangles making up the Region."
        nr_rects = ct.c_int()
        rects = pixman.pixman_region32_rectangles(ct.byref(self._region), ct.byref(nr_rects))
        nr_rects = nr_rects.value
        rects = ct.cast(rects, PIXMAN.box32_t_ptr)
        for i in range(nr_rects) :
            yield Rect.from_pixman_box(rects[i])
        #end for
    #end rectangles

    def __eq__(rgn1, rgn2) :
        "equality of two Regions."
        if not isinstance(rgn2, Region) :
            raise TypeError("args must be Regions")
        #end if
        return \
            pixman.pixman_region32_equal(ct.byref(rgn1._region), ct.byref(rgn2._region))
    #end __eq__

    def selfcheck(self) :
        if not pixman.pixman_region32_selfcheck(ct.byref(self._region)) :
            raise RuntimeError("Region failed Pixman selfcheck")
        #end if
        return \
            self
    #end selfcheck

    def reset(self, box) :
        "resets the Region to a simple rectangle."
        c_box = box.to_pixman_box()
        pixman.pixman_region32_reset(ct.byref(self._region), ct.byref(c_box))
        return \
            self
    #end reset

    def clear(self) :
        pixman.pixman_region32_clear(ct.byref(self._region))
    #end clear

#end Region

class Colour(qah.Colour) :
    "augment Colour with additional Pixman-specific functionality."

    __slots__ = () # to forestall typos

    @classmethod
    def from_pixman(celf, c) :
        alpha = c.alpha / 65535
        try :
            # convert from premultiplied alpha
            result = celf.from_rgba \
              ((
                c.red / 65535 / alpha,
                c.green / 65535 / alpha,
                c.blue / 65535 / alpha,
                alpha,
              ))
        except (ZeroDivisionError, OverflowError) :
            result = celf.from_rgba((0, 0, 0, alpha))
        #end try
        return \
            result
    #end from_pixman

    def to_pixman(self) :
        return \
            PIXMAN.color_t \
              ( # convert to premultiplied alpha
                red = round(self.r * self.a * 65535),
                green = round(self.g * self.a * 65535),
                blue = round(self.b * self.a * 65535),
                alpha = round(self.a * 65535),
              )
    #end to_pixman

#end Colour

class GradientStop :
    "representation of a Pixman gradient stop. x is a relative fraction in [0, 1] at which" \
    " the specified Colour is positioned."

    def __init__(self, x, colour) :
        if not isinstance(x, Number) or not isinstance(colour, Colour) :
            raise TypeError("invalid arg types")
        #end if
        self.x = x
        self.colour = colour
    #end __init__

    def __repr__(self) :
        return \
            "%s(%g, %s)" % (self.__class__.__name__, self.x, repr(self.colour))
    #end __repr__

    @staticmethod
    def from_pixman(gs) :
        return \
            GradientStop(PIXMAN.fixed_to_double(gs.x), Colour.from_pixman(gs.color))
    #end from_pixman

    def to_pixman(self) :
        return \
            PIXMAN.gradient_stop_t(PIXMAN.double_to_fixed(self.x), self.colour.to_pixman())
    #end to_pixman

    @staticmethod
    def to_pixman_array(stops) :
        "given a sequence of GradientStop objects, returns an array of Pixman" \
        " gradient_stop_t values along with the length of the array."
        nr_stops = len(stops)
        c_stops = (PIXMAN.gradient_stop_t * nr_stops)()
        for i in range(nr_stops) :
            c_stops[i] = stops[i].to_pixman()
        #end for
        return \
            c_stops, nr_stops
    #end to_pixman_array

#end GradientStop

def format_supported_destination(format) :
    "is the format with the specified code supported for destination images."
    return \
        pixman.pixman_format_supported_destination(format)
#end format_supported_destination

def format_supported_source(format) :
    "is the format with the specified code supported for source and mask images."
    return \
        pixman.pixman_format_supported_source(format)
#end format_supported_source

class Filter :
    "a Pixman filter type together with associated coefficients, if any. Do not" \
    " instantiate directly; use one of the create methods, or one of the predefined" \
    " instances FAST, GOOD, BEST, NEAREST or BILINEAR."

    __slots__ = ("_type", "_values", "_nr_values") # to forestall typos

    def __init__(self, _type, _values, _nr_values) :
        self._type = _type
        self._values = _values
        self._nr_values = _nr_values
    #end __init__

    def __del__(self) :
        if self._values != None :
            libc.free(self._values)
            self._values = None
        #end if
    #end __del__

    @staticmethod
    def create_convolution(dimensions, coeffs) :
        "creates a general convolution filter from a dimensions.x * dimensions.y array" \
        " of coefficients."
        width, height = Point.from_tuple(dimensions).assert_isshortint()
        nr_coeffs = len(coeffs)
        assert width > 0 and height > 0 and nr_coeffs == width * height
        c_values = libc.malloc((nr_coeffs + 2) * ct.sizeof(PIXMAN.fixed_t))
        if c_values == None :
            raise MemoryError("unable to allocate filter array")
        #end if
        cc_values = ct.cast(c_values, PIXMAN.fixed_t_ptr)
        cc_values[0] = PIXMAN.int_to_fixed(width)
        cc_values[1] = PIXMAN.int_to_fixed(height)
        for i in range(nr_coeffs) :
            cc_values[i + 2] = PIXMAN.double_to_fixed(coeffs[i])
        #end for
        return \
            Filter(PIXMAN.FILTER_CONVOLUTION, c_values, nr_coeffs + 2)
    #end create_convolution

    @staticmethod
    def create_resample(scale, reconstruct, sample, subsample_bits) :
        "creates a specific form of separable convolution filter (as a higher-quality" \
        " way of resampling images than the non-convolution filters) from the" \
        " specified settings: scale is a Point, reconstruct and sample are pairs" \
        " of PIXMAN.KERNEL_xxx values, and subsample_bits is a pair of integer number" \
        " of bits to shift for subpixel sampling."
        scale = Point.from_tuple(scale).to_pixman_fixed()
        subsample_bits = Point.from_tuple(subsample_bits).assert_isint()
        n_values = ct.c_int()
        values = pixman.pixman_filter_create_separable_convolution \
          (
            ct.byref(n_values),
            scale.x,
            scale.y,
            reconstruct[0],
            reconstruct[1],
            sample[0],
            sample[1],
            subsample_bits.x,
            subsample_bits.y,
          )
        if values == None :
            raise MemoryError("unable to allocate separable convolution filter")
        #end if
        return \
            Filter(PIXMAN.FILTER_SEPARABLE_CONVOLUTION, values, n_values.value)
    #end create_resample

#end Filter
# predefined filters:
Filter.FAST = Filter(PIXMAN.FILTER_FAST, None, 0)
Filter.GOOD = Filter(PIXMAN.FILTER_GOOD, None, 0)
Filter.BEST = Filter(PIXMAN.FILTER_BEST, None, 0)
Filter.NEAREST = Filter(PIXMAN.FILTER_NEAREST, None, 0)
Filter.BILINEAR = Filter(PIXMAN.FILTER_BILINEAR, None, 0)

def blt(src_bits, dst_bits, src_stride, dst_stride, src_bpp, dst_bpp, src_pos, dest_pos, dimensions) :
    "low-level blit routine. returns success/failure (i.e. unsupported format)."
    src_pos = Point.from_tuple(src_pos)
    dest_pos = Point.from_tuple(dest_pos)
    dimensions = Point.from_tuple(dimensions)
    return \
        pixman.pixman_blt(src_bits, dst_bits, src_stride, dst_stride, src_bpp, dst_bpp, src_pos.x, src_pos.y, dest_pos.x, dest_pos.y, dimensions.x, dimensions.y)
#end blt

def fill(bits, stride, bpp, pos, dimensions, filler) :
    "low-level fill routine. returns success/failure (i.e. unsupported format)."
    return \
        pixman.pixman_fill(bits, stride, bpp, pos.x, pos.y, dimensions.x, dimensions.y, filler)
#end fill

class Image :
    "wrapper for a Pixman image. Do not instantiate directly; use the create methods.\n" \
    "\n" \
    "An Image can consist of a two-dimensional array of pixels of some given size, which" \
    " can be both read (a source or mask) and written (a destination). Or it can consist" \
    " of some solid colour, or a gradient consisting of a given sequence of colours. Solid" \
    " and gradient images have no fixed extents, and can be sources or masks (?), but not" \
    " destinations."

    __slots__ = \
        (
            "_pmobj",
            "_arr",
            "_destroy_func",
            "_destroy_func_data",
            "_memory_read_func",
            "_memory_write_func",
            # need to keep references to ctypes-wrapped functions
            # so they don’t disappear prematurely:
            "_wrap_destroy_func",
            "_wrap_memory_read_func",
            "_wrap_memory_write_func",
        ) # to forestall typos

    def __init__(self, _pmobj) :
        self._pmobj = _pmobj
        self._arr = None
        self._destroy_func = None
        self._destroy_func_data = None
        self._memory_read_func = None
        self._memory_write_func = None
        self._wrap_destroy_func = None
        self._wrap_memory_read_func = None
        self._wrap_memory_write_func = None
    #end __init__

    def __del__(self) :
        if self._pmobj != None :
            pixman.pixman_image_unref(self._pmobj)
            self._pmobj = None
        #end if
    #end __del__

    @staticmethod
    def create_solid_fill(colour) :
        "creates an Image whose content consists of a single solid Colour."
        c_colour = colour.to_pixman()
        return \
            Image(pixman.pixman_image_create_solid_fill(ct.byref(c_colour)))
    #end create_solid_fill

    @staticmethod
    def create_linear_gradient(p1, p2, stops) :
        "creates an Image consisting of blends between the specified colours" \
        " along the line connecting the two given points. stops must be a sequence" \
        " of GradientStop objects."
        c_p1 = p1.to_pixman_fixed()
        c_p2 = p2.to_pixman_fixed()
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_linear_gradient(ct.byref(c_p1), ct.byref(c_p2), ct.byref(c_stops), nr_stops))
    #end create_linear_gradient

    @staticmethod
    def create_radial_gradient(inner, outer, inner_radius, outer_radius, stops) :
        "creates an Image consisting of blends between the specified colours" \
        " arranged radially between the two points and corresponding radii. stops" \
        " must be a sequence of GradientStop objects."
        c_inner = inner.to_pixman_fixed()
        c_outer = outer.to_pixman_fixed()
        c_inner_radius = PIXMAN.double_to_fixed(inner_radius)
        c_outer_radius = PIXMAN.double_to_fixed(outer_radius)
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_radial_gradient(ct.byref(c_inner), ct.byref(c_outer), c_inner_radius, c_outer_radius, ct.byref(c_stops), nr_stops))
    #end create_radial_gradient

    @staticmethod
    def create_conical_gradient(centre, angle, stops) :
        "creates an Image consisting of blends between the specified colours" \
        " arranged around a circle from the specified centre, starting and ending" \
        " at the specified angle. stops must be a sequence of GradientStop objects."
        # for consistency, I expect angle in radians, even though underlying
        # Pixman call wants it in degrees
        c_centre = centre.to_pixman_fixed()
        c_stops, nr_stops = GradientStop.to_pixman_array(stops)
        return \
            Image(pixman.pixman_image_create_conical_gradient(ct.byref(c_centre), PIXMAN.double_to_fixed(angle / qah.deg), ct.byref(c_stops), nr_stops))
    #end create_conical_gradient

    @staticmethod
    def create_bits(format, dimensions, bits = None, stride = 0, clear = True) :
        "low-level routine which expects bits to be a ctypes.c_void_p. clear is only" \
        " meaningful if bits is None, so Pixman allocates the bits. stride" \
        " is only meaningful if bits is not None."
        width, height = Point.from_tuple(dimensions).assert_isint()
        return \
            Image \
              (
                (pixman.pixman_image_create_bits_no_clear, pixman.pixman_image_create_bits)[clear]
                    (format, width, height, bits, stride)
              )
    #end create_bits

    @staticmethod
    def create_for_array(format, dimensions, arr, stride) :
        "creates an Image whose pixels reside in arr, which must be" \
        " a Python array.array object. format is a Pixman format code," \
        " dimensions is an integer Point specifying the dimensions of the" \
        " image, and stride specifies how many bytes each row of the image" \
        " occupies."
        width, height = Point.from_tuple(dimensions).assert_isint()
        address, length = arr.buffer_info()
        assert height * stride <= length * arr.itemsize
        result = Image \
          (
            pixman.pixman_image_create_bits_no_clear(format, width, height, address, stride)
              # thought I would use no_clear because array object will always be initialized
              # but in fact this makes no difference for caller-allocated bits
          )
        result._arr = arr # to ensure it doesn't go away prematurely
        return \
            result
    #end create_for_array

    @property
    def destroy_function(self) :
        "the destroy function and associated user data."
        return \
            (self._destroy_function, self._destroy_function_data)
    #end destroy_function

    @destroy_function.setter
    def destroy_function(self, destroy_function_and_data) :
        self.set_destroy_function(destroy_function_and_data[0], destroy_function_and_data[1])
    #end destroy_function

    def set_destroy_function(self, function, data) :
        "sets a new destroy_function. Useful for method chaining; otherwise just" \
        " assign to the destroy_function property."

        def wrap_destroy_function(_pmobj, _) :
            function(self, data)
        #end wrap_destroy_function

    #begin set_destroy_function
        self._destroy_function = function
        self._destroy_function_data = data
        self._wrap_destroy_function = PIXMAN.image_destroy_func_t(wrap_destroy_function)
        pixman.pixman_image_set_destroy_function(self._pmobj, self._wrap_destroy_function, None)
        return \
            self
    #end set_destroy_function

    def set_clip_region(self, region) :
        if not isinstance(region, Region) :
            raise TypeError("region must be a Region")
        #end if
        if not pixman.pixman_image_set_clip_region32(self._pmobj, ct.byref(region._pmregion)) :
            raise MemoryError("Pixman couldn’t set clip region")
        #end if
        return \
            self
    #end set_clip_region

    def set_has_client_clip(self, client_clip) :
        pixman.pixman_image_set_has_client_clip(self._pmobj, client_clip)
        return \
            self
    #end set_has_client_clip

    # TODO: set_transform

    def set_repeat(self, repeat) :
        "sets a new PIXMAN.REPEAT_xxx value, indicating what values to return when" \
        " trying to read pixels outside the image bounds."
        pixman.pixman_image_set_repeat(self._pmobj, repeat)
        return \
            self
    #end set_repeat

    def set_filter(self, filter) :
        "sets the filter, which must be a Filter object, to be applied to pixel values" \
        " read from the image."
        if not isinstance(filter, Filter) :
            raise TypeError("filter must be a Filter")
        #end if
        if not pixman.pixman_image_set_filter(self._pmobj, filter._type, filter._values, filter._nr_values) :
            raise RuntimeError("Pixman failed to set filter")
        #end if
        # Pixman copies the params array, so I don’t need to keep a reference
        return \
            self
    #end set_filter

    def set_source_clipping(self, source_clipping) :
        pixman.pixman_image_set_source_clipping(self._pmobj, source_clipping)
        return \
            self
    #end set_source_clipping

    def set_alpha_map(self, alpha_map, origin) :
        "specifies another Image from which to take the alpha channel, overriding" \
        " the one from this Image."
        if not isinstance(alpha_map, Image) :
            raise TypeError("alpha_map must be an Image")
        #end if
        origin = Point.from_tuple(origin).assert_isint()
        pixman.pixman_image_set_alpha_map(self._pmobj, alpha_map._pmobj, origin.x, origin.y)
        return \
            self
    #end set_alpha_map

    @property
    def component_alpha(self) :
        "whether the Image, when used as a mask, defines separate a, r, g, b alphas" \
        " as opposed to a common alpha."
        return \
            pixman.pixman_image_get_component_alpha(self._pmobj)
    #end component_alpha

    @component_alpha.setter
    def component_alpha(self, component_alpha) :
        self.set_component_alpha(component_alpha)
    #end component_alpha

    def set_component_alpha(self, component_alpha) :
        "sets a new component_alpha. Useful for method chaining; otherwise just" \
        " assign to the component_alpha property."
        pixman.pixman_image_set_component_alpha(self._pmobj, component_alpha)
        return \
            self
    #end set_component_alpha

    @property
    def read_memory_func(self) :
        "the memory-read accessor."
        return \
            self._memory_read_func
    #end read_memory_func

    @read_memory_func.setter
    def read_memory_func(self, read_func) :
        self.set_read_memory_func(read_func)
    #end read_memory_func

    def _set_accessors(self) :
        # actually calls Pixman to set the read and write accessors.
        pixman.pixman_image_set_accessors(self._pmobj, self._wrap_memory_read_func, self._wrap_memory_write_func)
        return \
            self
    #end _set_accessors

    def _set_read_memory_func(self, read_func) :
        self._memory_read_func = read_func
        self._wrap_memory_read_func = PIXMAN.read_memory_func_t(read_func)
    #end _set_read_memory_func

    def set_read_memory_func(self, read_func) :
        "sets a new memory-read accessor. Useful for method chaining; otherwise just" \
        " assign to the read_memory_func property."
        self._set_read_memory_func(read_func)
        return \
            self._set_accessors()
    #end set_read_memory_func

    @property
    def write_memory_func(self) :
        "the memory-write accessor."
        return \
            self._memory_write_func
    #end write_memory_func

    @write_memory_func.setter
    def write_memory_func(self, write_func) :
        self.set_write_memory_func(write_func)
    #end write_memory_func

    def _set_write_memory_func(self, write_func) :
        self._memory_write_func = write_func
        self._wrap_memory_write_func = PIXMAN.write_memory_func_t(write_func)
    #end _set_write_memory_func

    def set_write_memory_func(self, write_func) :
        "sets a new memory-write accessor. Useful for method chaining; otherwise just" \
        " assign to the write_memory_func property."
        self._set_write_memory_func(write_func)
        return \
            self._set_accessors()
    #end set_write_memory_func

    def set_accessors(self, read_func, write_func) :
        self._set_read_memory_func(read_func)
        self._set_write_memory_func(write_func)
        return \
            self._set_accessors()
    #end set_accessors

    # TODO: set_indexed

    @property
    def data(self) :
        return \
            pixman.pixman_image_get_data(self._pmobj)
    #end data

    @property
    def width(self) :
        return \
            pixman.pixman_image_get_width(self._pmobj)
    #end width

    @property
    def height(self) :
        return \
            pixman.pixman_image_get_height(self._pmobj)
    #end height

    @property
    def dimensions(self) :
        return \
            Point(self.width, self.height)
    #end dimensions

    @property
    def stride(self) :
        return \
            pixman.pixman_image_get_stride(self._pmobj)
    #end stride

    @property
    def depth(self) :
        return \
            pixman.pixman_image_get_depth(self._pmobj)
    #end depth

    @property
    def format(self) :
        return \
            pixman.pixman_image_get_format(self._pmobj)
    #end format

    def fill_rectangles(self, op, colour, rects) :
        "fills the specified sequence of rectangles using the given colour and operator."
        # actually calls pixman_image_fill_boxes. I can’t be bothered with
        # pixman_image_fill_rectangles because that only handles 16-bit coords.
        c_colour = colour.to_pixman()
        nr_boxes = len(rects)
        c_boxes = (PIXMAN.box32_t * nr_boxes)()
        for i in range(nr_boxes) :
            c_boxes[i] = rects[i].to_pixman_box()
        #end for
        if not pixman.pixman_image_fill_boxes(op, self._pmobj, ct.byref(c_colour), nr_boxes, ct.byref(c_boxes)) :
            raise MemoryError("pixman_image_fill_boxes failure")
        #end if
        return \
            self
    #end fill_rectangles

    # TODO: trapezoids

#end Image

def compute_composite_region(region, src, mask, dest, src_pos, mask_pos, dest_pos, dimensions) :
    # Note that Pixman does not (currently) provide a region32 version of this call.
    # Since I don’t want to add full region16 support just for this one call, I create
    # a temporary region16 and convert the result to the caller’s region32 afterwards.
    # Just to add insult to injury, the Pixman source code makes use of an internal
    # _pixman_compute_composite_region32 routine to do the work, then converts the
    # result to a region16 before returning it to us.
    if (
            not isinstance(src, Image)
        or
            mask != None and not isinstance(mask, Image)
        or
            not isinstance(dest, Image)
    ) :
        raise TypeError("image args must be Image objects")
    #end if
    tmp_region = PIXMAN.region16_t()
    src_pos = Point.from_tuple(src_pos).assert_isshortint()
    if mask != None or mask_pos != None :
        # “or”, not “and”: mask_pos must be specified if mask is specified
        mask_pos = Point.from_tuple(mask_pos).assert_isshortint()
    else :
        mask_pos = Point(0, 0) # dummy
    #end if
    dest_pos = Point.from_tuple(dest_pos).assert_isshortint()
    dimensions = Point.from_tuple(dimensions).assert_isshortint()
    pixman.pixman_region_init(ct.byref(tmp_region))
    if mask != None :
        c_mask = mask._pmobj
    else :
        c_mask = None
    #end if
    pixman.pixman_compute_composite_region(ct.byref(tmp_region), src._pmobj, c_mask, dest._pmobj, src_pos.x, src_pos.y, mask_pos.x, mask_pos.y, dest_pos.x, dest_pos.y, dimensions.x, dimensions.y)
      # returns false on empty region or allocation failure. Since I cannot distinguish
      # these two cases, I ignore the result.
    nr_rects = ct.c_int()
    rects16 = pixman.pixman_region_rectangles(ct.byref(self._region), ct.byref(nr_rects))
    nr_rects = nr_rects.value
    rects16 = ct.cast(rects16, PIXMAN.box16_t_ptr)
    Region.create_rects(list(Rect.from_pixman_box(rects16[i]) for i in range(nr_rects))).copy(region)
    pixman.pixman_region_fini(ct.byref(tmp_region))
#end compute_composite_region

def image_composite(op, src, mask, dest, src_pos, mask_pos, dest_pos, dimensions) :
    "composites the specified portions of Image src through Image mask (if not None)" \
    " onto Image dest according to operator op (a PIXMAN.OP_xxx value). src_pos is a" \
    " Point specifying the top left corner of the portion of src to read, mask_pos" \
    " similarly for mask (if not None), and dest_pos is the top left corner of dest" \
    " to store the result. dimensions is a Point defining the common dimensions" \
    " of the portions of all the images to use."
    if (
            not isinstance(src, Image)
        or
            mask != None and not isinstance(mask, Image)
        or
            not isinstance(dest, Image)
    ) :
        raise TypeError("image args must be Image objects")
    #end if
    src_pos = Point.from_tuple(src_pos).assert_isint()
    if mask != None or mask_pos != None :
        # “or”, not “and”: mask_pos must be specified if mask is specified
        mask_pos = Point.from_tuple(mask_pos).assert_isint()
    else :
        mask_pos = Point(0, 0) # dummy
    #end if
    dest_pos = Point.from_tuple(dest_pos).assert_isint()
    dimensions = Point.from_tuple(dimensions).assert_isint()
    if mask != None :
        c_mask = mask._pmobj
    else :
        c_mask = None
    #end if
    pixman.pixman_image_composite32(op, src._pmobj, c_mask, dest._pmobj, src_pos.x, src_pos.y, mask_pos.x, mask_pos.y, dest_pos.x, dest_pos.y, dimensions.x, dimensions.y)
#end image_composite

# TODO: glyphs

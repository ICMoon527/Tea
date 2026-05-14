class Styles:
    """GUI样式配置 - 生产级现代化设计"""

    is_dark_mode = False

    LIGHT_COLORS = {
        'PRIMARY_COLOR': '#5B8DEE',
        'PRIMARY_LIGHT': '#7BA3F1',
        'PRIMARY_DARK': '#3D6FD4',
        'SECONDARY_COLOR': '#10B981',
        'SECONDARY_LIGHT': '#34D399',
        'SECONDARY_DARK': '#059669',
        'ACCENT_COLOR': '#F59E0B',
        'BACKGROUND_COLOR': '#F8FAFC',
        'SURFACE_COLOR': '#FFFFFF',
        'TEXT_PRIMARY': '#1E293B',
        'TEXT_SECONDARY': '#64748B',
        'TEXT_MUTED': '#94A3B8',
        'HEADER_COLOR': '#1E293B',
        'TEXT_COLOR': '#333333',
        'BUTTON_HOVER_COLOR': '#3D6FD4',
        'BORDER_COLOR': '#E2E8F0',
        'BORDER_LIGHT': '#F1F5F9',
        'ERROR_COLOR': '#EF4444',
        'ERROR_LIGHT': '#FEE2E2',
        'SUCCESS_COLOR': '#10B981',
        'SUCCESS_LIGHT': '#D1FAE5',
        'WARNING_COLOR': '#F59E0B',
        'WARNING_LIGHT': '#FEF3C7',
    }

    DARK_COLORS = {
        'PRIMARY_COLOR': '#89b4fa',
        'PRIMARY_LIGHT': '#b4d0fb',
        'PRIMARY_DARK': '#74a0e0',
        'SECONDARY_COLOR': '#a6e3a1',
        'SECONDARY_LIGHT': '#c7f0c3',
        'SECONDARY_DARK': '#8bc78a',
        'ACCENT_COLOR': '#f9e2af',
        'BACKGROUND_COLOR': '#1e1e2e',
        'SURFACE_COLOR': '#2d2d44',
        'TEXT_PRIMARY': '#cdd6f4',
        'TEXT_SECONDARY': '#a6adc8',
        'TEXT_MUTED': '#6c7086',
        'HEADER_COLOR': '#cdd6f4',
        'TEXT_COLOR': '#cdd6f4',
        'BUTTON_HOVER_COLOR': '#585b70',
        'BORDER_COLOR': '#585b70',
        'BORDER_LIGHT': '#45475a',
        'ERROR_COLOR': '#f38ba8',
        'ERROR_LIGHT': '#3d2d3a',
        'SUCCESS_COLOR': '#a6e3a1',
        'SUCCESS_LIGHT': '#2d3d2d',
        'WARNING_COLOR': '#fab387',
        'WARNING_LIGHT': '#3d352d',
    }

    @classmethod
    def get_colors(cls):
        if cls.is_dark_mode:
            return cls.DARK_COLORS
        return cls.LIGHT_COLORS

    PRIMARY_COLOR = "#5B8DEE"
    PRIMARY_LIGHT = "#7BA3F1"
    PRIMARY_DARK = "#3D6FD4"
    SECONDARY_COLOR = "#10B981"
    SECONDARY_LIGHT = "#34D399"
    SECONDARY_DARK = "#059669"
    ACCENT_COLOR = "#F59E0B"

    BACKGROUND_COLOR = "#F8FAFC"
    SURFACE_COLOR = "#FFFFFF"
    TEXT_PRIMARY = "#1E293B"
    TEXT_SECONDARY = "#64748B"
    TEXT_MUTED = "#94A3B8"
    HEADER_COLOR = "#1E293B"
    TEXT_COLOR = "#333333"
    BUTTON_HOVER_COLOR = "#3D6FD4"

    BORDER_COLOR = "#E2E8F0"
    BORDER_LIGHT = "#F1F5F9"

    ERROR_COLOR = "#EF4444"
    ERROR_LIGHT = "#FEE2E2"
    SUCCESS_COLOR = "#10B981"
    SUCCESS_LIGHT = "#D1FAE5"
    WARNING_COLOR = "#F59E0B"
    WARNING_LIGHT = "#FEF3C7"

    HEADER_FONT = ("微软雅黑", 28, "bold")
    SUB_HEADER_FONT = ("微软雅黑", 20, "bold")
    TITLE_FONT = ("微软雅黑", 16)
    BUTTON_FONT = ("微软雅黑", 13)
    LABEL_FONT = ("微软雅黑", 11)
    TEXT_FONT = ("微软雅黑", 10)

    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32
    SPACING_2XL = 48

    PADY_LARGE = 32
    PADY_MEDIUM = 24
    PADY_SMALL = 12
    PADX_LARGE = 48
    PADX_MEDIUM = 24
    PADX_SMALL = 12

    BUTTON_WIDTH = 22
    BUTTON_HEIGHT = 2
    ENTRY_WIDTH = 32
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 700
    DIALOG_WIDTH = 680
    DIALOG_HEIGHT = 480

    WINDOW_SIZES = {
        "large":    (1100, 680),
        "medium":   (800, 550),
        "small":    (500, 350),
    }

    RADIUS_SM = 4
    RADIUS_MD = 8
    RADIUS_LG = 12
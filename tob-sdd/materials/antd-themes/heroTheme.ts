import type { ThemeConfig } from 'antd';
import { theme } from 'antd';

const { defaultAlgorithm, darkAlgorithm } = theme;

/** HeroUI Dashboard 风格 - 亮色主题 */
export const heroLightTheme: ThemeConfig = {
  algorithm: defaultAlgorithm,
  token: {
    // 主色（接近 HeroUI 蓝色）
    colorPrimary: '#006FEE',
    colorSuccess: '#17C964',
    colorWarning: '#F5A524',
    colorError: '#F31260',
    colorInfo: '#006FEE',

    // 背景与表面
    colorBgLayout: '#F4F4F5',
    colorBgContainer: '#FFFFFF',
    colorBgElevated: '#FFFFFF',
    colorBgSpotlight: '#F4F4F5',

    // 文字
    colorText: '#11181C',
    colorTextSecondary: '#687076',
    colorTextTertiary: '#889096',
    colorTextQuaternary: '#C1C8CD',

    // 边框与圆角
    colorBorder: '#E4E4E7',
    colorBorderSecondary: '#F4F4F5',
    borderRadius: 12,
    borderRadiusLG: 16,
    borderRadiusSM: 8,

    // 字体与尺寸
    fontSize: 14,
    fontSizeLG: 16,
    fontSizeSM: 12,
    controlHeight: 40,
    controlHeightLG: 48,
    controlHeightSM: 32,

    // 阴影（轻量）
    boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02)',
    boxShadowSecondary: '0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05)',
  },
  components: {
    Layout: {
      siderBg: '#FFFFFF',
      headerBg: '#FFFFFF',
      bodyBg: '#F4F4F5',
    },
    Menu: {
      itemBg: 'transparent',
      itemSelectedBg: '#E6F1FE',
      itemSelectedColor: '#006FEE',
      itemHoverBg: '#F4F4F5',
      itemBorderRadius: 10,
    },
    Card: {
      borderRadiusLG: 16,
      paddingLG: 24,
    },
    Button: {
      borderRadius: 10,
      controlHeight: 40,
      fontWeight: 500,
    },
    Table: {
      headerBg: '#F4F4F5',
      headerColor: '#687076',
      rowHoverBg: '#F4F4F5',
      borderColor: '#E4E4E7',
    },
    Input: {
      borderRadius: 10,
      activeBorderColor: '#006FEE',
    },
  },
};

/** HeroUI Dashboard 风格 - 暗色主题 */
export const heroDarkTheme: ThemeConfig = {
  algorithm: darkAlgorithm,
  token: {
    colorPrimary: '#006FEE',
    colorSuccess: '#17C964',
    colorWarning: '#F5A524',
    colorError: '#F31260',
    colorInfo: '#006FEE',

    colorBgLayout: '#09090B',
    colorBgContainer: '#18181B',
    colorBgElevated: '#27272A',
    colorBgSpotlight: '#27272A',

    colorText: '#ECEDEE',
    colorTextSecondary: '#A1A1AA',
    colorTextTertiary: '#71717A',
    colorTextQuaternary: '#52525B',

    colorBorder: '#27272A',
    colorBorderSecondary: '#3F3F46',
    borderRadius: 12,
    borderRadiusLG: 16,
    borderRadiusSM: 8,

    fontSize: 14,
    controlHeight: 40,
  },
  components: {
    Layout: {
      siderBg: '#18181B',
      headerBg: '#18181B',
      bodyBg: '#09090B',
    },
    Menu: {
      itemBg: 'transparent',
      itemSelectedBg: '#006FEE20',
      itemSelectedColor: '#006FEE',
      itemHoverBg: '#27272A',
      itemBorderRadius: 10,
    },
    Card: {
      borderRadiusLG: 16,
      colorBgContainer: '#18181B',
    },
    Button: {
      borderRadius: 10,
      controlHeight: 40,
    },
    Table: {
      headerBg: '#27272A',
      headerColor: '#A1A1AA',
      rowHoverBg: '#27272A',
      borderColor: '#3F3F46',
    },
  },
};

/** 主题集合（方便切换） */
export const heroThemes = {
  light: heroLightTheme,
  dark: heroDarkTheme,
} as const;

export type HeroThemeKey = keyof typeof heroThemes;
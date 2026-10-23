import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import {legacyRedirects} from './redirects';

// GitHub Pages проекта: https://ivbeg.github.io/book-govngo/
// Тот же префикс зашит в static/*.html для старых адресов mdBook.
const SITE_BASE = '/book-govngo/';

const config: Config = {
  title: 'Государственные НКО и их открытость',
  tagline: 'Как отличить государственную НКО, посчитать её и увидеть, какие нормы на неё не действуют',
  favicon: 'img/favicon.svg',

  url: 'https://ivbeg.github.io',
  baseUrl: SITE_BASE,
  organizationName: 'ivbeg',
  projectName: 'book-govngo',
  trailingSlash: true,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'ru',
    locales: ['ru'],
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  themes: [
    '@docusaurus/theme-mermaid',
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['ru'],
        docsRouteBasePath: '/',
        indexBlog: false,
        highlightSearchTermsOnTargetPage: true,
      },
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: legacyRedirects,
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          showLastUpdateTime: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    docs: {
      sidebar: {
        hideable: true,
      },
    },
    navbar: {
      title: 'Государственные НКО',
      logo: {
        alt: 'Государственные НКО',
        src: 'img/favicon.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'bookSidebar',
          position: 'left',
          label: 'Книга',
        },
        {
          to: '/#с-чего-начать',
          label: 'С чего начать',
          position: 'left',
          activeBaseRegex: '^$',
        },
        {
          to: '/appendices/glossary/',
          label: 'Глоссарий',
          position: 'left',
        },
        {
          href: 'https://github.com/ivbeg/book-govngo',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Книга',
          items: [
            {label: 'О книге', to: '/'},
            {label: 'Граница понятия', to: '/boundary/what-it-is/'},
            {label: 'Как узнать организацию', to: '/identification/methods/'},
            {label: 'Федеральный бюджет', to: '/finance/federal/'},
            {label: 'Открытость', to: '/openness/overview/'},
            {label: 'Что менять', to: '/policy/decisions/'},
          ],
        },
        {
          title: 'Справочник',
          items: [
            {label: 'Глоссарий', to: '/appendices/glossary/'},
            {label: 'Коды видов расходов', to: '/appendices/kvr/'},
            {label: 'Крупнейшие получатели, 2019', to: '/appendices/federal-top-2019/'},
            {label: 'Источники', to: '/appendices/sources/'},
            {label: 'Прежние адреса', to: '/appendices/old-addresses/'},
          ],
        },
      ],
      copyright: '© 2026 Иван Бегтин. Цифры книги относятся к 2018–2020 годам.',
    },
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

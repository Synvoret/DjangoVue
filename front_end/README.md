# front_end

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```


<!-- project structure -->
src/
    assets/ (static assets, images, fonts, etc.)
    components/ (reusable components)
        common/ (common components for the entire project)
        layout/ (layout components header, footer ...)
        specific/ (view-specific components)
    hooks/ (hooks, useFetch, useAuth)
    views/ (views, pages)
        Home.vue (home page)
        About.vue (about view)
        ... (others views)
    router/ (router configuration)
        index.js (main router cofiguration)
    styles/ (global styles)
        main.css (main styles)
    utils/ (helper functions)
        helpers.js (helper function)
    App.vue (main apllication components)
    main.js (main input file)

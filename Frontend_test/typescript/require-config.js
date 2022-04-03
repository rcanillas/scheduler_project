require.config({
    paths: {
        'knockout': '../node_modules/knockout/build/output/knockout-latest'
    }
});
require(['../typescript/main']); // run main.ts from here.

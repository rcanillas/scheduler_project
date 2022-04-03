define(["require", "exports", "knockout"], function (require, exports, ko) {
    "use strict";
    exports.__esModule = true;
    var ViewModel = /** @class */ (function () {
        function ViewModel() {
            this.words = ko.observableArray(['Hello', 'World']);
        }
        return ViewModel;
    }());
    ko.applyBindings(new ViewModel());
});

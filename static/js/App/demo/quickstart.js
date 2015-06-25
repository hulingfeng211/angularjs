/**
 * Created by george on 15-6-25.
 */
angular.module('demoApp', ['mgcrea.ngStrap']).controller('quickStartController', function ($scope, $http) {
    $http.get('/demo').success(function(response){
        $scope.names=response;
});
        $scope.modal = {
            "title": "Title",
            "content": "Hello Modal<br />This is a multiline message!"
        };
        $scope.friends = [
            {name: 'tom', age: 16},
            {name: 'jerry', age: 20},
            {name: 'garfield', age: 22}
        ];
    }
);

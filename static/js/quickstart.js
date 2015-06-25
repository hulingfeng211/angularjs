/**
 * Created by george on 15-6-25.
 */

angular.module('http1App',[]).controller('httpController',function($scope,$http){
    $http.get('/demo').success(function(response){
        $scope.names=response;
    });
});
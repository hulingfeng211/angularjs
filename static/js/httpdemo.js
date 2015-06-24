/**
 *
 * Created by george on 15-6-24.
 */
angular.module('httpApp',[]).controller('httpController',function($scope,$http){
    $http.get('/demo').success(function(response){
        $scope.names=response;
    });
});

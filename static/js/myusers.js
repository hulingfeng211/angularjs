/**
 * Created by george on 15-6-24.
 */
angular.module('myapp', []).controller('userctrl', function ($scope, $http) {
    $scope.fName = '';
    $scope.lName = '';
    $scope.passw1 = '';
    $scope.passw2 = '';
    $scope.edit = true;
    $scope.error = false;
    $scope.incomplete = false;
    $scope.loadData = function () {
        $http.get('/user/list').success(function (response) {
            $scope.users = response;
        });

    };
    $scope.loadData();
    $scope.saveUser = function () {

        var user = {
            _id: $scope._id,
            fName: $scope.fName,
            lName: $scope.lName
        };
        $http.post('/user', user).success(function (response) {
                $scope.loadData();
            }
        );
        $scope._id = '';
        $scope.fName = '';
        $scope.lName = '';
        $scope.incomplete = false;

    };
    $scope.deleteUser=function(id){
        $http.delete('/user/'+id).success(function(response){
              $scope.loadData();
        })  ;
    };

    $scope.editUser = function (id) {
        if (id == '') {
            $scope.edit = true;
            $scope.incomplete = true;
            $scope._id='';
            $scope.fName = '';
            $scope.lName = '';
        } else {
            $scope.edit = true;
            angular.forEach($scope.users, function (user, index) {
                if (user._id == id) {
                    $scope._id = id;
                    $scope.fName = user.fName;
                    $scope.lName = user.lName;
                }
            });
        }
    };

    $scope.$watch('passw1', function () {
        $scope.test();
    });
    $scope.$watch('passw2', function () {
        $scope.test();
    });
    $scope.$watch('fName', function () {
        $scope.test();
    });
    $scope.$watch('lName', function () {
        $scope.test();
    });

    $scope.test = function () {
        if ($scope.passw1 !== $scope.passw2) {
            $scope.error = true;
        } else {
            $scope.error = false;
        }
        $scope.incomplete = true;
        console.log('aaaa');
        if ($scope.edit && ($scope.fName.length > 0 && $scope.lName.length > 0 && $scope.passw1.length > 0 && $scope.passw2.length > 0)) {
            $scope.incomplete = false;
        }
    };

});
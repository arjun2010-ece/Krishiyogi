(function(){


var app = angular.module("Farmer", []);

app.controller("FarmCtrl",function($scope,$http){

    $scope.FarmerJson=[];
    $scope.fetchFarmer=function(){
			      $http.get('/api/farmershelp/')
			      .then(function(response){
			       $scope.FarmerJson = response.data;
			      });

    };

   $scope.FarmJson=[];
    $scope.fetchFarms=function(){
		      $http.get('/api/farmershelp/farms')
		      .then(function(response){
		       $scope.FarmJson = response.data;
		      });
    };

    $scope.FieldJson=[];
    $scope.fetchFields=function(){
		      $http.get('/api/farmershelp/fields')
		      .then(function(response){
		       $scope.FieldJson = response.data;
		      });
    };



   
});

})();
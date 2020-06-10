var portfolioApp = angular.module('portfolioApp',[]);

portfolioApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  });

portfolioApp.controller('GalleryListCtrl',GalleryListCtrl);
portfolioApp.controller('HeaderCtrl',HeaderCtrl);
function GalleryListCtrl($http){

    var vm = this;

    $http.get('./json/galleries.json').then(function(response){
        vm.galleries=response.data;
    });
    $http.get('./json/sortTypes.json').then(function(response){
        vm.sortList = response.data;
        vm.orderProp=vm.sortList[1];
    });
    }
function HeaderCtrl($http){
    var hd = this;
    $http.get('./json/headers.json').then(function(response){
        hd.list = response.data;
    });

}


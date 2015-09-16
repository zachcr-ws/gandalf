'use strict';

/**
 * Config for the router
 */
angular.module('app')
  .run(
    [          '$rootScope', '$state', '$stateParams',
      function ($rootScope,   $state,   $stateParams) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;        
      }
    ]
  )
  .config(
    [          '$stateProvider', '$urlRouterProvider',
      function ($stateProvider,   $urlRouterProvider) {
          
          $urlRouterProvider
              .otherwise('/app/total');
          $stateProvider
              .state('app', {
                  abstract: true,
                  url: '/app',
                  templateUrl: 'static/tpl/app.html'
              })
              .state('app.total', {
                  url: '/total',
                  templateUrl: 'static/tpl/app_total.html',
                  resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load(['static/js/controllers/chart.js']);
                    }]
                  }
              })
              .state('app.success', {
                url: '/success',
                templateUrl: 'static/tpl/app_success.html',
                resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load(['static/vendor/angular/angular-bootstrap/ui-bootstrap-tpls.js',
                          'static/css/pretty-json.css',
                          'static/vendor/libs/pretty-json-min.js']);
                    }]
                  }
              })
              .state('app.delay', {
                url: '/delay',
                templateUrl: 'static/tpl/app_delay.html',
                resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load([
                          'static/css/pretty-json.css',
                          'static/vendor/libs/pretty-json-min.js'
                        ]);
                    }]
                  }
              })
              .state('app.launching', {
                url: '/launching',
                templateUrl: 'static/tpl/app_launching.html',
                resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load([
                          'static/css/pretty-json.css',
                          'static/vendor/libs/pretty-json-min.js'
                        ]);
                    }]
                  }
              })
              .state('app.failed', {
                url: '/failed',
                templateUrl: 'static/tpl/app_failed.html',
                resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load([
                          'static/css/pretty-json.css',
                          'static/vendor/libs/pretty-json-min.js'
                        ]);
                    }]
                  }
              })
              .state('app.tasks', {
                url: '/tasks',
                templateUrl: 'static/tpl/app_tasks.html',
                resolve: {
                    deps: ['$ocLazyLoad',
                      function( $ocLazyLoad ){
                        return $ocLazyLoad.load([
                          'static/css/pretty-json.css',
                          'static/vendor/libs/pretty-json-min.js'
                        ]);
                    }]
                  }
              })
      }
    ]
  );
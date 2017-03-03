#! /usr/bin/env node

var requestPromise = require('request-promise')
    , promises = require('promises')
    , fs = require('fs')
    , ObjectID = require('mongodb').ObjectID
    , MongoClient = require('mongodb').MongoClient
    , http = require('http')
    , wappalyzer = require('@wappalyzer/wappalyzer');

MongoClient.connect('mongodb://127.0.0.1:27017/ipstats', (err, db) => {
    mongodb = db;
    var IpBanners = db.collection('ips_banners');
    var cursor = IpBanners.find({});
    cursor.each(function(err, item) {
        if(item != null) {
            if (item.ports != null)
            {
                var ports = item.ports;
                for (let i = 0; i < ports.length; i++)
                {
                    console.log(ports[i]);
                }
                setTimeout(() => {}, 3000);
            }
        };
      });
//    .then(result => {
//        console.log(result);
//    });
});

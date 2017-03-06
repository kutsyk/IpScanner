function getCurrentTabUrl(callback) {
    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function (tabs) {
        var tab = tabs[0];

        var url = tab.url;
        console.assert(typeof url == 'string', 'tab.url should be a string');
        callback(url);
    });

}

function sendWhoisRequest(url, success, error) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: success,
        error: error,
        beforeSend: setHeader
    });

    function setHeader(xhr) {
        xhr.setRequestHeader('Accept', 'application/json');
    }
}

function getBaseWebsiteInfo(searchTerm, callback, errorCallback) {
    var getIP = 'https://freegeoip.net/json/' + encodeURIComponent(searchTerm);
    var ripeUrl = 'https://rest.db.ripe.net/search?source=ripe&query-string=';
    var arinUrl = 'https://whois.arin.net/rest/ip/';

    $.getJSON(getIP, function (data) {
        var ip = data.ip;
        ripeUrl += ip;
        arinUrl += ip;
        var cc = data.country_code.toLowerCase();
        var country = data.country_name;
        chrome.browserAction.setIcon({path: '/flag_icons/png/' + cc + '.png'});
        sendWhoisRequest(ripeUrl, function (ripeData) {

                var person = {};
                var objects = ripeData.objects.object;
                console.log(ripeData);
                for (var i = 0; i < objects.length; i++) {
                    if (objects[i].type == "person") {
                        // console.log(objects[i]);
                        var attr = objects[i].attributes.attribute;
                        // console.log("ATTR");
                        // console.log(attr);
                        for (var j = 0; j < attr.length; j++) {
                            if (attr[j].name == "person")
                                person.name = attr[j].value;

                            if (attr[j].name == "phone")
                                person.phone = attr[j].value;
                        }
                        // console.log(person);
                    }
                }
                data.whois = person;
                chrome.storage.local.set({cache: data, cacheTime: Date.now()}, function() {
                    callback(data);
                });
                // callback(data);
            },
            function (ripeError) {
                sendWhoisRequest(arinUrl, function (arinData) {
                        data.whois = arinData;
                       callback(data);
                    },
                    function (arinError) {
                        console.log('error');
                    });
            });
    });

}

function renderStatus(statusText) {
    OPENED = false;
    document.getElementById('status').textContent = statusText;
}

function RenderView(data) {
        console.log(data);
        var ip = data.ip;
        var city = data.city;
        var country = data.country_name;
        var owner = data.whois.name;
        var phone = data.whois.phone;
        renderStatus(ip);

        var ipO = document.getElementById('ip');
        var phoneO = document.getElementById('phone');
        var ownerO = document.getElementById('hoster');
        var addressO = document.getElementById('address');

        ipO.textContent = ip;
        phoneO.textContent = phone;
        ownerO.textContent = owner;
        addressO.textContent = country + ', ' + city;
        // chrome.storage.sync.set({'synced': true}, function() {
        // Notify that we saved.
        // console.log('Settings saved');
        // });
}

document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabUrl(function (url) {
        pathArray = url.split('/');
        host = pathArray[2];
        url = host;
        // Put the image URL in Google search.
        renderStatus('Collecting info ' + url);

        chrome.storage.local.get(['cache', 'cacheTime'], function (items) {
            console.log(items);
            if (items.cache && items.cacheTime && items.cacheTime) {
                console.log(items.cacheTime);
                if (items.cacheTime > Date.now() - 4 * 3600 * 1000) {
                    console.log("if block: ");
                    console.log(items.cacheTime);
                    return getBaseWebsiteInfo(url, RenderView); // Serialization is auto, so nested objects are no problem
                }
                else
                    RenderView(items.cache);
            }
            getBaseWebsiteInfo(url, RenderView)
        });
    });
});

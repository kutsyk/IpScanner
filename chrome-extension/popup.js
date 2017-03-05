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
                for (var i = 0; i < objects.length; i++)
                {
                    if (objects[i].type == "person")
                    {
                        console.log(objects[i]);
                        var attr = objects[i].attributes.attribute;
                        console.log("ATTR");
                        console.log(attr);
                        for (var j = 0; j < attr.length; j++)
                        {
                            if (attr[j].name == "person")
                                person.name = attr.value;

                            if (attr[j].name == "phone")
                                person.phone = attr.value;
                        }
                        console.log(person);
                    }
                }
                data.whois = ripeData;
                callback(data);
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

document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabUrl(function (url) {
        pathArray = url.split('/');
        host = pathArray[2];
        url = host;
        // Put the image URL in Google search.
        renderStatus('Collecting info ' + url);

        getBaseWebsiteInfo(url, function (data) {
            var ip = data.ip;
            var city = data.city;
            var country = data.country_name;
            renderStatus(ip);

            var ipO = document.getElementById('ip');
            var ownerO = document.getElementById('hoster');
            var addressO = document.getElementById('address');

            ipO.textContent = ip;
            ownerO.textContent = "unknown";
            addressO.textContent = country + ', ' + city;
            // chrome.storage.sync.set({'synced': true}, function() {
                // Notify that we saved.
                // console.log('Settings saved');
            // });
        }, function (errorMessage) {
            renderStatus('Cannot display status. ' + errorMessage);
        });
    });
});

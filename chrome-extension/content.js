window.onload = function () {
    chrome.runtime.sendMessage({greeting: "hello"}, function (response) {
            var url = response.url;
            var pathArray = url.split('/');
            var host = pathArray[2];

            if (host) {
                // url = url.replace("http://", "");
                // url = url.replace("https://", "");
                // Put the image URL in Google search.
                getBaseWebsiteInfo(host);
            }
        }
    );
};


// chrome.tabs.onActivated.addListener(function (tabId, windowId) {

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
// });
// chrome.runtime.onMessage.addListener(
//     function (request, sender, sendResponse) {
//         console.log(sender.tab ?
//         "from a content script:" + sender.tab.url :
//             "from the extension");
//         if (request.greeting == "hello")
//             sendResponse({url: sender.tab ? sender.tab.url : ""});
//     });


function sendWhoisRequest(url, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.send();
    var data = JSON.parse(xhr.responseText);
    success(data);
}

function getBaseWebsiteInfo(searchTerm) {
    var getIP = 'https://freegeoip.net/json/' + searchTerm;
    var ripeUrl = 'https://rest.db.ripe.net/search?source=ripe&query-string=';
    var arinUrl = 'https://whois.arin.net/rest/ip/';

    var xhr = new XMLHttpRequest();
    xhr.open("GET", getIP, false);
    xhr.send();
    var data = JSON.parse(xhr.responseText);

    // function getIPQ(data) {
    console.log(data);
    var ip = data.ip;
    ripeUrl += ip;
    arinUrl += ip;
    var cc = data.country_code.toLowerCase();
    var country = data.country_name;
    chrome.runtime.sendMessage({changeIcon: true, country_code: cc});
    // chrome.browserAction.setIcon({path: '/flag_icons/png/' + cc + '.png'});
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
            chrome.storage.local.set({cache: data, cacheTime: Date.now()}, function () {
            });
            // callback(data);
        },
        function (ripeError) {
            sendWhoisRequest(arinUrl, function (arinData) {
                    data.whois = arinData;
                },
                function (arinError) {
                    console.log('error');
                });
        });
    // };
}


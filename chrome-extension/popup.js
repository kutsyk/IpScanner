// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;
    console.assert(typeof url == 'string', 'tab.url should be a string');
    callback(url);
  });

}

/**
 * @param {string} searchTerm - Search term for Google Image search.
 * @param {function(string,number,number)} callback - Called when an image has
 *   been found. The callback gets the URL, width and height of the image.
 * @param {function(string)} errorCallback - Called when the image is not found.
 *   The callback gets a string that describes the failure reason.
 */
function getBaseWebsiteInfo(searchTerm, callback, errorCallback) {
  // Google image search - 100 searches per day.
  // https://developers.google.com/image-search/
  var searchUrl = 'https://freegeoip.net/json/' + encodeURIComponent(searchTerm);
  $.getJSON( searchUrl, callback);

}

function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
    pathArray = url.split( '/' );
    host = pathArray[2];
    url = host;
    // Put the image URL in Google search.
    renderStatus('Collecting info ' + url);

    getBaseWebsiteInfo(url, function(baseInfo) {

      console.log(baseInfo);

      renderStatus('Info for: ' + url);

      var ip = document.getElementById('ip');
      var country = document.getElementById('country');
      var city = document.getElementById('city');

      ip.textContent = baseInfo['ip'];
      country.textContent = baseInfo['country_name'];
      city.textContent = baseInfo['city'];

    }, function(errorMessage) {
      renderStatus('Cannot display status. ' + errorMessage);
    });
  });
});

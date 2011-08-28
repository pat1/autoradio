/**
 * Open
 *
 * Popup window utility for creating pop up windows without intrusive using any
 * intrusive code.
 *
 * 
 */
(function ($) {

    $.open = {};

    // Default popup window parameters
    $.open.defaultParams = {
        "width":       "800",   // Window width
        "height":      "600",   // Window height
        "top":         "0",     // Y offset (in pixels) from top of screen
        "left":        "0",     // X offset (in pixels) from left side of screen
        "directories": "no",    // Show directories/Links bar?
        "location":    "no",    // Show location/address bar?
        "resizeable":  "yes",   // Make the window resizable?
        "menubar":     "no",    // Show the menu bar?
        "toolbar":     "no",    // Show the tool (Back button etc.) bar?
        "scrollbars":  "yes",   // Show scrollbars?
        "status":      "no"     // Show the status bar?
    };


    // Some configuration properties
    $.open.defaultConfig = {
        autoFocus: true
    };


    // Open popup window static function
    $.open.newWindow = function (href, params, config) {

        // Popup window defaults (don't leave it to the browser)
        var windowParams = $.extend($.open.defaultParams, params);

        // Configuration properties
        var windowConfig = $.extend($.open.defaultConfig, config);

        var windowName = params["windowName"] || "new_window";

        var i, paramString = "";

        for (i in windowParams) {
            if (windowParams.hasOwnProperty(i)) {
                paramString += (paramString === "") ? "" : ",";
                paramString += i + "=";

                // Allow true/false instead of yes/no in params
                if (windowParams[i] === true || windowParams[i] === false) {
                    paramString += (windowParams[i]) ? "yes" : "no";
                }
                else {
                    paramString += windowParams[i];
                }
            }
        }

        var popupWindow = window.open(href, windowName, paramString);

        if (windowConfig.autoFocus) {
            popupWindow.focus();
        }

        return popupWindow;
    };


    // Plugin method: $("...").popup()
    $.fn.open = function (parameters, callback) {

        var params = parameters.params || parameters;
        var config = parameters.config || {};

        // Loop over all matching elements
        this.each(function (){

            // Add an onClick behavior to this element
            $(this).click(function (event) {

                // Prevent the browser's default onClick handler
                event.preventDefault();

                // Use the target attribute as the window name
                if ($(this).attr("target")) {
                    params.windowName = $(this).attr("target");
                }

                // Determine the url to open
                //   Use param.href over element's href
                var href;
                if (params.href) {
                    href = params.href;
                }
                else if ($(this).attr("href")) {
                    href = $(this).attr("href");
                }
                else {
                    return;  // Can't openWindow anything, so stop here
                }

                
                // Pop up the window
                var windowObject = $.open.newWindow(href, params, config);

                if (callback) {
                    callback(windowObject);
                }
            });
        });

        return $;
    };

})(jQuery);
// https://docs.djangoproject.com/en/3.2/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function UpdateUTCDateTime() {
  $("#server-clock").html(moment.utc().format("DD/MM/YYYY hh:mm"));
  setTimeout(UpdateUTCDateTime, 60 * 1000);
}

jQuery(document).ready(() => {
  UpdateUTCDateTime();
});

function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand("copy");
    var msg = successful ? "successful" : "unsuccessful";
    console.log("Fallback: Copying text command was " + msg);
  } catch (err) {
    console.error("Fallback: Oops, unable to copy", err);
  }

  document.body.removeChild(textArea);
}
function copyTextToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(
    function () {
      console.log("Async: Copying to clipboard was successful!");
    },
    function (err) {
      console.error("Async: Could not copy text: ", err);
    }
  );
}

(function ($) {
  showSuccessToast = function (message, title = "") {
    resetToastPosition();
    $.toast({
      heading: title,
      text: message,
      showHideTransition: "slide",
      icon: "success",
      loaderBg: "#f96868",
      position: "top-right",
    });
  };
  showInfoToast = function (message, title = "") {
    resetToastPosition();
    $.toast({
      heading: title,
      text: message,
      showHideTransition: "slide",
      icon: "info",
      loaderBg: "#46c35f",
      position: "top-right",
    });
  };
  showWarningToast = function (message, title = "") {
    resetToastPosition();
    $.toast({
      heading: title,
      text: message,
      showHideTransition: "slide",
      icon: "warning",
      loaderBg: "#57c7d4",
      position: "top-right",
    });
  };
  showDangerToast = function (message, title = "") {
    resetToastPosition();
    $.toast({
      heading: title,
      text: message,
      showHideTransition: "slide",
      icon: "error",
      loaderBg: "#f2a654",
      position: "top-right"
    });
  };
  showToastPosition = function (position) {
    resetToastPosition();
    $.toast({
      heading: "Positioning",
      text: "Specify the custom position object or use one of the predefined ones",
      position: String(position),
      icon: "info",
      stack: false,
      loaderBg: "#f96868",
    });
  };
  showToastInCustomPosition = function () {
    resetToastPosition();
    $.toast({
      heading: "Custom positioning",
      text: "Specify the custom position object or use one of the predefined ones",
      icon: "info",
      position: {
        left: 120,
        top: 120,
      },
      stack: false,
      loaderBg: "#f96868",
    });
  };
  resetToastPosition = function () {
    $(".jq-toast-wrap").removeClass("bottom-left bottom-right top-left top-right mid-center"); // to remove previous position class
    $(".jq-toast-wrap").css({
      top: "",
      left: "",
      bottom: "",
      right: "",
    }); //to remove previous position style
  };
})(jQuery);

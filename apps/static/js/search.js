var batch_list_const = [];
var areaf1_list_const = [];
var areaf2_list_const = [];
var areaf3_list_const = [];
var areaf4_list_const = [];
var areaf5_list_const = [];
var state_list_const = [];
var city_list_const = [];
var gender_list_const = [];
var page_num = 0;
var page_len = 0;
jQuery(document).ready(function () {
  $("#search_result").hide();
  $(".circle-loader").hide();

  init_batch_selection();
  init_gender_selection();

  $("#areaf1").click(function () {
    if (batch_list_const.length == 0)
      showWarningToast("Please select the batches", "Notification");
  });

  $("#areaf2").click(function () {
    if (areaf1_list_const.length == 0)
      showWarningToast("Please select the areaf1", "Notification");
  });

  $("#areaf3").click(function () {
    if (areaf2_list_const.length == 0)
      showWarningToast("Please select the areaf2", "Notification");
  });

  $("#areaf4").click(function () {
    if (areaf3_list_const.length == 0)
      showWarningToast("Please select the areaf3", "Notification");
  });

  $("#areaf5").click(function () {
    if (areaf4_list_const.length == 0)
      showWarningToast("Please select the areaf4", "Notification");
  });

  $("#state").click(function () {
    if (areaf5_list_const.length == 0)
      showWarningToast("Please select the areaf5", "Notification");
  });

  $("#city").click(function () {
    if (areaf5_list_const.length == 0)
      showWarningToast("Please select the areaf5", "Notification");
  });
});

///////////////////////Batch Selection///////////////////////////
function init_batch_selection() {
  $("#batch_search").on("keyup", function () {
    var search = $(this).val().toLowerCase();
    $(".batch-list").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
    });
    var len = $(".batch-list:visible").length;
    if (len) $(".batch-check").show();
    else $(".batch-check").hide();
    check_batch();
  });
  $("#any_batch").change(function () {
    if ($(this).prop("checked"))
      $(".batch-list:visible input").prop("checked", true);
    else $(".batch-list:visible input").prop("checked", false);
    check_batch();
  });
  $(".batch-list input").change(function () {
    check_batch();
  });
  input_list = $(".batch-list input");
  var checked_len = input_list.length;
  $("#selected_batch_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < checked_len; i++) {
    if (show) {
      buf = $("#selected_batch_num").text();
      if (i == 0)
        $("#selected_batch_num").text(
          buf + input_list.eq(i).attr("batch_name")
        );
      else
        $("#selected_batch_num").text(
          buf + " / " + input_list.eq(i).attr("batch_name")
        );
      if ($("#selected_batch_num").width() > $("#batch").width() - 130) {
        show = false;
        $("#selected_batch_num").text(buf);
      } else {
        show_num = i + 1;
      }
    }
    batch_list_const.push(input_list.eq(i).attr("batch_id"));
  }
  if (checked_len == 0) $("#selected_batch_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_batch_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_batch_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  update_batch();
}

function check_batch() {
  batch_list_const = [];
  input_list = $(".batch-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_batch_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_batch_num").text();
        if (checked_len == 0)
          $("#selected_batch_num").text(
            buf + input_list.eq(i).attr("batch_name")
          );
        else
          $("#selected_batch_num").text(
            buf + " / " + input_list.eq(i).attr("batch_name")
          );
        if ($("#selected_batch_num").width() > $("#batch").width() - 130) {
          show = false;
          $("#selected_batch_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      batch_list_const.push(input_list.eq(i).attr("batch_id"));
    }
  }
  if (checked_len == 0) $("#selected_batch_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_batch_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_batch_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_batch").prop("checked", true);
  else $("#any_batch").prop("checked", false);
  update_batch();
}

function update_batch() {
  postData = {
    object: "batch", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];
        areaf1_list = data["areaf1_list"];
        init_areaf1_selection(areaf1_list);
        init_areaf2_selection();
        init_areaf3_selection();
        init_areaf4_selection();
        init_areaf5_selection();
        init_state_selection();
        init_city_selection();

        // $('#zip_code').empty('')
        // zipcode_list = data['zipcode_list']
        // len = zipcode_list.length
        // for(i = 0; i < len; i++)
        // {
        //   var optionElement = document.createElement('option')
        //   optionElement.setAttribute('disabled', 'disabled')
        //   optionElement.setAttribute('value', zipcode_list[i]['Zipcode'])
        //   optionElement.innerText = zipcode_list[i]['Zipcode']
        //   $('#zip_code').append(optionElement)
        // }

        // $('#area_code').empty('')
        // area_code_list = data['area_code_list']
        // len = area_code_list.length
        // var optionElement = document.createElement('option')
        // optionElement.setAttribute('disabled', 'disabled')
        // optionElement.innerText = 'Examples:'
        // $('#area_code').append(optionElement)
        // for(i = 0; i < len; i++)
        // {
        //   optionElement = document.createElement('option')
        //   optionElement.setAttribute('value', area_code_list[i]['Area_code'])
        //   optionElement.innerText = area_code_list[i]['Area_code']
        //   $('#area_code').append(optionElement)
        // }
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
///////////////////////////////////////////////////////////////////////

///////////////////////Areaf1 Selection///////////////////////////////
function init_areaf1_selection(areaf1_list = []) {
  areaf1_list_const = [];
  $("#areaf1_selection").empty();
  $("#selected_areaf1_num").text(0);

  var len = areaf1_list.length;
  if (len) {
    $("#areaf1").removeClass('btn-danger');
    $("#areaf1").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="areaf1_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf1-check"></div>';
    appendHTML += '<div class="dropdown-item areaf1-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_areaf1"> Any Areaf1';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf1-check"></div>';
    for (i = 0; i < len; i++) {
      var each = areaf1_list[i];
      appendHTML += '<div class="dropdown-item areaf1-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["Areaf1"] + '" areaf1="' +
        (each["Areaf1"] == '' ? 'Other' : each["Areaf1"]) +
        '"> ' +
        (each["Areaf1"] == '' ? 'Other' : each["Areaf1"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#areaf1_selection").append(appendHTML);

    $("#areaf1_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".areaf1-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".areaf1-list:visible").length;
      if (len) $(".areaf1-check").show();
      else $(".areaf1-check").hide();
      check_areaf1();
    });

    $("#any_areaf1").change(function () {
      if ($(this).prop("checked"))
        $(".areaf1-list:visible input").prop("checked", true);
      else $(".areaf1-list:visible input").prop("checked", false);
      check_areaf1();
    });
    $(".areaf1-list input").change(function () {
      check_areaf1();
    });

    input_list = $(".areaf1-list input");
    var checked_len = input_list.length;
    $("#selected_areaf1_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_areaf1_num").text();
        if (i == 0)
          $("#selected_areaf1_num").text(buf + input_list.eq(i).attr("areaf1"));
        else
          $("#selected_areaf1_num").text(
            buf + " / " + input_list.eq(i).attr("areaf1")
          );
        if ($("#selected_areaf1_num").width() > $("#areaf1").width() - 130) {
          show = false;
          $("#selected_areaf1_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      areaf1_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_areaf1_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_areaf1_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_areaf1_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_areaf1();
  }
  else {
    $("#areaf1").removeClass('btn-success');
    $("#areaf1").addClass('btn-danger');
  }
}

function check_areaf1() {
  areaf1_list_const = [];
  input_list = $(".areaf1-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_areaf1_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_areaf1_num").text();
        if (checked_len == 0)
          $("#selected_areaf1_num").text(buf + input_list.eq(i).attr("areaf1"));
        else
          $("#selected_areaf1_num").text(
            buf + " / " + input_list.eq(i).attr("areaf1")
          );
        if ($("#selected_areaf1_num").width() > $("#areaf1").width() - 130) {
          show = false;
          $("#selected_areaf1_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      areaf1_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_areaf1_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_areaf1_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_areaf1_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_areaf1").prop("checked", true);
  else $("#any_areaf1").prop("checked", false);
  update_areaf1();
}

function update_areaf1() {
  postData = {
    object: "areaf1", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        areaf2_list = data["areaf2_list"];
        init_areaf2_selection(areaf2_list);
        init_areaf3_selection();
        init_areaf4_selection();
        init_areaf5_selection();
        init_state_selection();
        init_city_selection();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////Areaf2 Selection///////////////////////////////
function init_areaf2_selection(areaf2_list = []) {
  areaf2_list_const = [];
  $("#areaf2_selection").empty();
  $("#selected_areaf2_num").text(0);

  var len = areaf2_list.length;
  if (len) {
    $("#areaf2").removeClass('btn-danger');
    $("#areaf2").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="areaf2_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf2-check"></div>';
    appendHTML += '<div class="dropdown-item areaf2-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_areaf2"> Any Areaf2';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf2-check"></div>';
    for (i = 0; i < len; i++) {
      var each = areaf2_list[i];
      appendHTML += '<div class="dropdown-item areaf2-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["Areaf2"] + '" areaf2="' +
        (each["Areaf2"] == '' ? 'Other' : each["Areaf2"]) +
        '"> ' +
        (each["Areaf2"] == '' ? 'Other' : each["Areaf2"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#areaf2_selection").append(appendHTML);

    $("#areaf2_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".areaf2-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".areaf2-list:visible").length;
      if (len) $(".areaf2-check").show();
      else $(".areaf2-check").hide();
      check_areaf2();
    });

    $("#any_areaf2").change(function () {
      if ($(this).prop("checked"))
        $(".areaf2-list:visible input").prop("checked", true);
      else $(".areaf2-list:visible input").prop("checked", false);
      check_areaf2();
    });
    $(".areaf2-list input").change(function () {
      check_areaf2();
    });

    input_list = $(".areaf2-list input");
    var checked_len = input_list.length;
    $("#selected_areaf2_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_areaf2_num").text();
        if (i == 0)
          $("#selected_areaf2_num").text(buf + input_list.eq(i).attr("areaf2"));
        else
          $("#selected_areaf2_num").text(
            buf + " / " + input_list.eq(i).attr("areaf2")
          );
        if ($("#selected_areaf2_num").width() > $("#areaf2").width() - 130) {
          show = false;
          $("#selected_areaf2_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      areaf2_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_areaf2_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_areaf2_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_areaf2_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_areaf2();
  }
  else {
    $("#areaf2").removeClass('btn-success');
    $("#areaf2").addClass('btn-danger');
  }
}

function check_areaf2() {
  areaf2_list_const = [];
  input_list = $(".areaf2-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_areaf2_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_areaf2_num").text();
        if (checked_len == 0)
          $("#selected_areaf2_num").text(buf + input_list.eq(i).attr("areaf2"));
        else
          $("#selected_areaf2_num").text(
            buf + " / " + input_list.eq(i).attr("areaf2")
          );
        if ($("#selected_areaf2_num").width() > $("#areaf2").width() - 130) {
          show = false;
          $("#selected_areaf2_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      areaf2_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_areaf2_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_areaf2_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_areaf2_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_areaf2").prop("checked", true);
  else $("#any_areaf2").prop("checked", false);
  update_areaf2();
}

function update_areaf2() {
  postData = {
    object: "areaf2", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        areaf3_list = data["areaf3_list"];
        init_areaf3_selection(areaf3_list);
        init_areaf4_selection();
        init_areaf5_selection();
        init_state_selection();
        init_city_selection();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////Areaf3 Selection///////////////////////////////
function init_areaf3_selection(areaf3_list = []) {
  areaf3_list_const = [];
  $("#areaf3_selection").empty();
  $("#selected_areaf3_num").text(0);

  var len = areaf3_list.length;
  if (len) {
    $("#areaf3").removeClass('btn-danger');
    $("#areaf3").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="areaf3_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf3-check"></div>';
    appendHTML += '<div class="dropdown-item areaf3-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_areaf3"> Any Areaf3';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf3-check"></div>';
    for (i = 0; i < len; i++) {
      var each = areaf3_list[i];
      appendHTML += '<div class="dropdown-item areaf3-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["Areaf3"] + '" areaf3="' +
        (each["Areaf3"] == '' ? 'Other' : each["Areaf3"]) +
        '"> ' +
        (each["Areaf3"] == '' ? 'Other' : each["Areaf3"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#areaf3_selection").append(appendHTML);

    $("#areaf3_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".areaf3-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".areaf3-list:visible").length;
      if (len) $(".areaf3-check").show();
      else $(".areaf3-check").hide();
      check_areaf3();
    });

    $("#any_areaf3").change(function () {
      if ($(this).prop("checked"))
        $(".areaf3-list:visible input").prop("checked", true);
      else $(".areaf3-list:visible input").prop("checked", false);
      check_areaf3();
    });
    $(".areaf3-list input").change(function () {
      check_areaf3();
    });

    input_list = $(".areaf3-list input");
    var checked_len = input_list.length;
    $("#selected_areaf3_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_areaf3_num").text();
        if (i == 0)
          $("#selected_areaf3_num").text(buf + input_list.eq(i).attr("areaf3"));
        else
          $("#selected_areaf3_num").text(
            buf + " / " + input_list.eq(i).attr("areaf3")
          );
        if ($("#selected_areaf3_num").width() > $("#areaf3").width() - 130) {
          show = false;
          $("#selected_areaf3_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      areaf3_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_areaf3_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_areaf3_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_areaf3_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_areaf3();
  }
  else {
    $("#areaf3").removeClass('btn-success');
    $("#areaf3").addClass('btn-danger');
  }
}

function check_areaf3() {
  areaf3_list_const = [];
  input_list = $(".areaf3-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_areaf3_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_areaf3_num").text();
        if (checked_len == 0)
          $("#selected_areaf3_num").text(buf + input_list.eq(i).attr("areaf3"));
        else
          $("#selected_areaf3_num").text(
            buf + " / " + input_list.eq(i).attr("areaf3")
          );
        if ($("#selected_areaf3_num").width() > $("#areaf3").width() - 130) {
          show = false;
          $("#selected_areaf3_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      areaf3_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_areaf3_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_areaf3_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_areaf3_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_areaf3").prop("checked", true);
  else $("#any_areaf3").prop("checked", false);
  update_areaf3();
}

function update_areaf3() {
  postData = {
    object: "areaf3", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
    areaf3_list: areaf3_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        areaf4_list = data["areaf4_list"];
        init_areaf4_selection(areaf4_list);
        init_areaf5_selection();
        init_state_selection();
        init_city_selection();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////Areaf4 Selection///////////////////////////////
function init_areaf4_selection(areaf4_list = []) {
  areaf4_list_const = [];
  $("#areaf4_selection").empty();
  $("#selected_areaf4_num").text(0);

  var len = areaf4_list.length;
  if (len) {
    $("#areaf4").removeClass('btn-danger');
    $("#areaf4").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="areaf4_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf4-check"></div>';
    appendHTML += '<div class="dropdown-item areaf4-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_areaf4"> Any Areaf4';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf4-check"></div>';
    for (i = 0; i < len; i++) {
      var each = areaf4_list[i];
      appendHTML += '<div class="dropdown-item areaf4-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["Areaf4"] + '" areaf4="' +
        (each["Areaf4"] == '' ? 'Other' : each["Areaf4"]) +
        '"> ' +
        (each["Areaf4"] == '' ? 'Other' : each["Areaf4"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#areaf4_selection").append(appendHTML);

    $("#areaf4_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".areaf4-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".areaf4-list:visible").length;
      if (len) $(".areaf4-check").show();
      else $(".areaf4-check").hide();
      check_areaf4();
    });

    $("#any_areaf4").change(function () {
      if ($(this).prop("checked"))
        $(".areaf4-list:visible input").prop("checked", true);
      else $(".areaf4-list:visible input").prop("checked", false);
      check_areaf4();
    });
    $(".areaf4-list input").change(function () {
      check_areaf4();
    });

    input_list = $(".areaf4-list input");
    var checked_len = input_list.length;
    $("#selected_areaf4_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_areaf4_num").text();
        if (i == 0)
          $("#selected_areaf4_num").text(buf + input_list.eq(i).attr("areaf4"));
        else
          $("#selected_areaf4_num").text(
            buf + " / " + input_list.eq(i).attr("areaf4")
          );
        if ($("#selected_areaf4_num").width() > $("#areaf4").width() - 130) {
          show = false;
          $("#selected_areaf4_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      areaf4_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_areaf4_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_areaf4_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_areaf4_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_areaf4();
  }
  else {
    $("#areaf4").removeClass('btn-success');
    $("#areaf4").addClass('btn-danger');
  }
}

function check_areaf4() {
  areaf4_list_const = [];
  input_list = $(".areaf4-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_areaf4_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_areaf4_num").text();
        if (checked_len == 0)
          $("#selected_areaf4_num").text(buf + input_list.eq(i).attr("areaf4"));
        else
          $("#selected_areaf4_num").text(
            buf + " / " + input_list.eq(i).attr("areaf4")
          );
        if ($("#selected_areaf4_num").width() > $("#areaf4").width() - 130) {
          show = false;
          $("#selected_areaf4_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      areaf4_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_areaf4_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_areaf4_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_areaf4_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_areaf4").prop("checked", true);
  else $("#any_areaf4").prop("checked", false);
  update_areaf4();
}

function update_areaf4() {
  postData = {
    object: "areaf4", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
    areaf3_list: areaf3_list_const,
    areaf4_list: areaf4_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        areaf5_list = data["areaf5_list"];
        init_areaf5_selection(areaf5_list);
        init_state_selection();
        init_city_selection();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////Areaf5 Selection///////////////////////////////
function init_areaf5_selection(areaf5_list = []) {
  areaf5_list_const = [];
  $("#areaf5_selection").empty();
  $("#selected_areaf5_num").text(0);

  var len = areaf5_list.length;
  if (len) {
    $("#areaf5").removeClass('btn-danger');
    $("#areaf5").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="areaf5_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf5-check"></div>';
    appendHTML += '<div class="dropdown-item areaf5-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_areaf5"> Any Areaf5';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider areaf5-check"></div>';
    for (i = 0; i < len; i++) {
      var each = areaf5_list[i];
      appendHTML += '<div class="dropdown-item areaf5-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["Areaf5"] + '" areaf5="' +
        (each["Areaf5"] == '' ? 'Other' : each["Areaf5"]) +
        '"> ' +
        (each["Areaf5"] == '' ? 'Other' : each["Areaf5"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#areaf5_selection").append(appendHTML);

    $("#areaf5_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".areaf5-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".areaf5-list:visible").length;
      if (len) $(".areaf5-check").show();
      else $(".areaf5-check").hide();
      check_areaf5();
    });

    $("#any_areaf5").change(function () {
      if ($(this).prop("checked"))
        $(".areaf5-list:visible input").prop("checked", true);
      else $(".areaf5-list:visible input").prop("checked", false);
      check_areaf5();
    });
    $(".areaf5-list input").change(function () {
      check_areaf5();
    });

    input_list = $(".areaf5-list input");
    var checked_len = input_list.length;
    $("#selected_areaf5_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_areaf5_num").text();
        if (i == 0)
          $("#selected_areaf5_num").text(buf + input_list.eq(i).attr("areaf5"));
        else
          $("#selected_areaf5_num").text(
            buf + " / " + input_list.eq(i).attr("areaf5")
          );
        if ($("#selected_areaf5_num").width() > $("#areaf5").width() - 130) {
          show = false;
          $("#selected_areaf5_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      areaf5_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_areaf5_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_areaf5_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_areaf5_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_areaf5();
  }
  else {
    $("#areaf5").removeClass('btn-success');
    $("#areaf5").addClass('btn-danger');
  }
}

function check_areaf5() {
  areaf5_list_const = [];
  input_list = $(".areaf5-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_areaf5_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_areaf5_num").text();
        if (checked_len == 0)
          $("#selected_areaf5_num").text(buf + input_list.eq(i).attr("areaf5"));
        else
          $("#selected_areaf5_num").text(
            buf + " / " + input_list.eq(i).attr("areaf5")
          );
        if ($("#selected_areaf5_num").width() > $("#areaf5").width() - 130) {
          show = false;
          $("#selected_areaf5_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      areaf5_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_areaf5_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_areaf5_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_areaf5_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_areaf5").prop("checked", true);
  else $("#any_areaf5").prop("checked", false);
  update_areaf5();
}

function update_areaf5() {
  postData = {
    object: "areaf5", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
    areaf3_list: areaf3_list_const,
    areaf4_list: areaf4_list_const,
    areaf5_list: areaf5_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        state_list = data["state_list"];
        init_state_selection(state_list);
        init_city_selection();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////User State Selection///////////////////////////////
function init_state_selection(state_list = []) {
  state_list_const = [];
  $("#state_selection").empty();
  $("#selected_state_num").text(0);

  var len = state_list.length;
  if (len) {
    $("#state").removeClass('btn-danger');
    $("#state").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="state_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider state-check"></div>';
    appendHTML += '<div class="dropdown-item state-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_state"> Any State';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider state-check"></div>';
    for (i = 0; i < len; i++) {
      var each = state_list[i];
      appendHTML += '<div class="dropdown-item state-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["State"] + '" state="' +
        (each["State"] == '' ? 'Unknown' : each["State"]) +
        '"> ' +
        (each["State"] == '' ? 'Unknown' : each["State"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#state_selection").append(appendHTML);

    $("#state_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".state-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".state-list:visible").length;
      if (len) $(".state-check").show();
      else $(".state-check").hide();
      check_state();
    });

    $("#any_state").change(function () {
      if ($(this).prop("checked"))
        $(".state-list:visible input").prop("checked", true);
      else $(".state-list:visible input").prop("checked", false);
      check_state();
    });
    $(".state-list input").change(function () {
      check_state();
    });

    input_list = $(".state-list input");
    var checked_len = input_list.length;
    $("#selected_state_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_state_num").text();
        if (i == 0)
          $("#selected_state_num").text(buf + input_list.eq(i).attr("state"));
        else
          $("#selected_state_num").text(
            buf + " / " + input_list.eq(i).attr("state")
          );
        if ($("#selected_state_num").width() > $("#state").width() - 130) {
          show = false;
          $("#selected_state_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      state_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_state_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_state_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_state_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
    update_state();
  }
  else {
    $("#state").removeClass('btn-success');
    $("#state").addClass('btn-danger');
  }
}

function check_state() {
  state_list_const = [];
  input_list = $(".state-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_state_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_state_num").text();
        if (checked_len == 0)
          $("#selected_state_num").text(buf + input_list.eq(i).attr("state"));
        else
          $("#selected_state_num").text(
            buf + " / " + input_list.eq(i).attr("state")
          );
        if ($("#selected_state_num").width() > $("#state").width() - 130) {
          show = false;
          $("#selected_state_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      state_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_state_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_state_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_state_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_state").prop("checked", true);
  else $("#any_state").prop("checked", false);
  update_state();
}

function update_state() {
  postData = {
    object: "state", //batch, areaf1, areaf2, ...
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
    areaf3_list: areaf3_list_const,
    areaf4_list: areaf4_list_const,
    areaf5_list: areaf5_list_const,
    state_list: state_list_const,
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        data = result["data"];

        city_list = data["city_list"];
        init_city_selection(city_list);
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
//////////////////////////////////////////////////////////////////////

///////////////////////User City Selection///////////////////////////////
function init_city_selection(city_list = []) {
  city_list_const = [];
  $("#city_selection").empty();
  $("#selected_city_num").text(0);

  var len = city_list.length;
  if (len) {
    $("#city").removeClass('btn-danger');
    $("#city").addClass('btn-success');
    var appendHTML = "";
    appendHTML += '<div class="dropdown-header search-box">';
    appendHTML +=
      '<input id="city_search" type="text" class="form-control form-contrl-sm" placeholder="Search...">';
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider city-check"></div>';
    appendHTML += '<div class="dropdown-item city-check">';
    appendHTML += '<div class="form-check-group">';
    appendHTML += '<label class="form-check-label">';
    appendHTML +=
      '<input type="checkbox" checked class="form-check-input" id="any_city"> Any City';
    appendHTML += "</label>";
    appendHTML += "</div>";
    appendHTML += "</div>";
    appendHTML += '<div class="dropdown-divider city-check"></div>';
    for (i = 0; i < len; i++) {
      var each = city_list[i];
      appendHTML += '<div class="dropdown-item city-list">';
      appendHTML += '<div class="form-check-group">';
      appendHTML += '<label class="form-check-label">';
      appendHTML +=
        '<input type="checkbox" checked class="form-check-input" name="' + each["City"] + '" city="' +
        (each["City"] == '' ? 'Unknown' : each["City"]) +
        '"> ' +
        (each["City"] == '' ? 'Unknown' : each["City"]) +
        " (" +
        each["product_num"] +
        ")";
      appendHTML += "</label>";
      appendHTML += "</div>";
      appendHTML += "</div>";
    }
    $("#city_selection").append(appendHTML);

    $("#city_search").on("keyup", function () {
      var search = $(this).val().toLowerCase();
      $(".city-list").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1);
      });
      var len = $(".city-list:visible").length;
      if (len) $(".city-check").show();
      else $(".city-check").hide();
      check_city();
    });

    $("#any_city").change(function () {
      if ($(this).prop("checked"))
        $(".city-list:visible input").prop("checked", true);
      else $(".city-list:visible input").prop("checked", false);
      check_city();
    });
    $(".city-list input").change(function () {
      check_city();
    });

    input_list = $(".city-list input");
    var checked_len = input_list.length;
    $("#selected_city_num").text("");
    var buf = "";
    var show_num = 0;
    var show = true;
    for (i = 0; i < checked_len; i++) {
      if (show) {
        buf = $("#selected_city_num").text();
        if (i == 0)
          $("#selected_city_num").text(buf + input_list.eq(i).attr("city"));
        else
          $("#selected_city_num").text(
            buf + " / " + input_list.eq(i).attr("city")
          );
        if ($("#selected_city_num").width() > $("#city").width() - 130) {
          show = false;
          $("#selected_city_num").text(buf);
        } else {
          show_num = i + 1;
        }
      }
      city_list_const.push(input_list.eq(i).attr("name"));
    }
    if (checked_len == 0) $("#selected_city_num").text("(0 selected)");
    else if (show_num == 0)
      $("#selected_city_num").text(
        buf + "(+" + (checked_len - show_num) + " selected)"
      );
    else if (show_num < checked_len)
      $("#selected_city_num").text(
        buf + " /(+" + (checked_len - show_num) + " selected)"
      );
  }
  else {
    $("#city").removeClass('btn-success');
    $("#city").addClass('btn-danger');
  }
}

function check_city() {
  city_list_const = [];
  input_list = $(".city-list:visible input");
  var len = input_list.length;
  var checked_len = 0;
  $("#selected_city_num").text("");
  var buf = "";
  var show_num = 0;
  var show = true;
  for (i = 0; i < len; i++) {
    if (input_list.eq(i).prop("checked")) {
      if (show) {
        buf = $("#selected_city_num").text();
        if (checked_len == 0)
          $("#selected_city_num").text(buf + input_list.eq(i).attr("city"));
        else
          $("#selected_city_num").text(
            buf + " / " + input_list.eq(i).attr("city")
          );
        if ($("#selected_city_num").width() > $("#city").width() - 130) {
          show = false;
          $("#selected_city_num").text(buf);
        } else {
          show_num = checked_len + 1;
        }
      }
      checked_len++;
      city_list_const.push(input_list.eq(i).attr("name"));
    }
  }
  if (checked_len == 0) $("#selected_city_num").text("(0 selected)");
  else if (show_num == 0)
    $("#selected_city_num").text(
      buf + "(+" + (checked_len - show_num) + " selected)"
    );
  else if (show_num < checked_len)
    $("#selected_city_num").text(
      buf + " /(+" + (checked_len - show_num) + " selected)"
    );
  if (checked_len == len) $("#any_city").prop("checked", true);
  else $("#any_city").prop("checked", false);
}
//////////////////////////////////////////////////////////////////////

///////////////////////User Gender Selection///////////////////////////////
function init_gender_selection() {
  $("#any_gender").change(function () {
    if ($(this).prop("checked"))
      $("#gender_selection input").prop("checked", true);
    else $("#gender_selection input").prop("checked", false);
  });
  $("#gender_selection input").change(function () {
    if ($(this).attr("id") == "any_gender") check_gender();
    else {
      if ($("#any_gender").prop("checked"))
        $("#any_gender").prop("checked", false);
      else {
        input_list = $("#gender_selection input");
        var len = input_list.length;
        for (i = 1; i < len; i++) {
          if (!input_list.eq(i).prop("checked")) {
            $("#any_gender").prop("checked", false);
            break;
          }
        }
        if (i == len) $("#any_gender").prop("checked", true);
      }
      check_gender();
    }
  });
  check_gender();
}

function check_gender() {
  gender_list_const = [];
  input_list = $("#gender_selection input");
  var checked_len = input_list.length;
  var num_text = "";
  for (i = 1; i < checked_len; i++) {
    if (input_list.eq(i).prop("checked"))
    {
      if (num_text == "") num_text += input_list.eq(i).attr("gender");
      else num_text += " / " + input_list.eq(i).attr("gender");
      gender_list_const.push(input_list.eq(i).attr("gender"));
    }
  }
  if (num_text == "") num_text = "(0 selected)";
  $("#selected_gender_num").text(num_text);
}
//////////////////////////////////////////////////////////////////////

function show_result(page = 0) {
  if (batch_list_const == []) {
    showWarningToast("Please select the batch", "Notification");
    return;
  }
  if (gender_list_const == []) {
    showWarningToast("Please select the gender", "Notification");
    return;
  }

  area_code_list = $("#area_code").val();
  if (area_code_list == "") area_code_list = [];
  else area_code_list = area_code_list.split("\n");

  zipcode_list = $("#zip_code").val();
  if (zipcode_list == "") zipcode_list = [];
  else zipcode_list = zipcode_list.split("\n");
  $("#search_result").show();
  $("#search_result .table tbody").empty();
  $("#pagination").hide();

  postData = {
    area_code_list: area_code_list,
    zipcode_list: zipcode_list,
    batch_list: batch_list_const,
    areaf1_list: areaf1_list_const,
    areaf2_list: areaf2_list_const,
    areaf3_list: areaf3_list_const,
    areaf4_list: areaf4_list_const,
    areaf5_list: areaf5_list_const,
    state_list: state_list_const,
    city_list: city_list_const,
    gender_list: gender_list_const,
    price_min: $("#price_min").val(),
    price_max: $("#price_max").val(),
    extra1: $("#extra1").is(":checked"),
    extra2: $("#extra2").is(":checked"),
    extra3: $("#extra3").is(":checked"),
    extra4: $("#extra4").is(":checked"),
    extra5: $("#extra5").is(":checked"),
    page: page,
  };
  $(".circle-loader").show();
  $.ajax({
    url: "/search_result",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      $(".circle-loader").hide();
      var state = result["state"];
      if (state == "OK") {
        var product_list = result["data"];
        $("#records_num").text(result["length"] + " records found");
        console.log(product_list);
        page_num = page;
        var len = result["length"];
        if (len) {
          product_list.forEach(function (each) {
            each["Extra1"] = each["Extra1"] == null ? "" : "Extra1 included";
            each["Extra2"] = each["Extra2"] == null ? "" : "Extra2 included";
            each["Extra3"] = each["Extra3"] == null ? "" : "Extra3 included";
            each["Extra4"] = each["Extra4"] == null ? "" : "Extra4 included";
            each["Extra5"] = each["Extra5"] == null ? "" : "Extra5 included";
            each["Extra"] = "";
            each["Extra"] += each["Extra1"];
            each["Extra"] +=
              each["Extra1"] == "" ? each["Extra2"] : "<br>" + each["Extra2"];
            each["Extra"] +=
              each["Extra2"] == "" ? each["Extra3"] : "<br>" + each["Extra3"];
            each["Extra"] +=
              each["Extra3"] == "" ? each["Extra4"] : "<br>" + each["Extra4"];
            each["Extra"] +=
              each["Extra4"] == "" ? each["Extra5"] : "<br>" + each["Extra5"];

            var appendHTML = "";
            appendHTML += "<tr>";
            appendHTML +=
              '<td class="text-center">' + (each["Area_code"] || '') + "</td>";
            appendHTML +=
              '<td class="text-center">' +
              (each["Exp_day"] ? (each["Exp_day"] + "/") : '') +
              (each["Exp_month"] || '') +
              "/" +
              (each["Exp_year"] || '') +
              "</td>";
            appendHTML +=
              "<td>" +
              (each["Areaf1"] || '') +
              "<br>" +
              (each["Areaf2"] || '') +
              "<br>" +
              (each["Areaf3"] || '') +
              "<br>" +
              (each["Areaf4"] || '') +
              "</td>";
            if(each["Areaf6"])
              appendHTML +=
                '<td class="text-center"><img src="static/assets/vendors/flag-icon-css/flags/4x3/' +
                each["Areaf6"] +
                '.svg" alt="' +
                each["Areaf6"] +
                '.svg"><br>' +
                (each["Areaf5"] || '') +
                "</td>";
            else
              appendHTML +=
                '<td class="text-center">' +
                (each["Areaf5"] || '') +
                "</td>";
            appendHTML +=
              "<td>" +
              (each["City"] || '') +
              "<br>" +
              (each["State"] || '') +
              "<br>" +
              (each["Zipcode"] || '') +
              "</td>";
            appendHTML += "<td>" + (each["First_name"] || '') + "</td>";
            appendHTML += '<td class="text-center">' + (each["Gender"] || '') + "</td>";
            appendHTML += '<td class="text-center">' + (each["Extra"] || '') + "</td>";
            var Batch_Publish_date = new Date(each["Batch_Publish_date"]);
            appendHTML +=
              "<td>" +
              (each["Batch_id"] || '') +
              "<br>" +
              (each["Batch_Name"] || '') +
              "<br>" +
              Batch_Publish_date.getDate().toString().padStart(2, "0") +
              "/" +
              (Batch_Publish_date.getMonth() + 1).toString().padStart(2, "0") +
              "/" +
              Batch_Publish_date.getFullYear() +
              "</td>";
            appendHTML += '<td class="text-right">' + (each["Price"] || '') + "$</td>";
            if (each["Sold_unsold"] == "ON_CART")
              appendHTML +=
                '<td class="text-center"><button type="button" class="btn btn-warning" onclick="remove_product(' +
                each["id"] +
                ')"><i class="mdi mdi-cart-minus cart-icon"></i></button></td>';
            else
              appendHTML +=
                '<td class="text-center"><button type="button" class="btn btn-success" onclick="add_product(' +
                each["id"] +
                ')"><i class="mdi mdi-cart-plus cart-icon"></i></button></td>';
            appendHTML += "</tr>";
            $("#search_result .table tbody").append(appendHTML);
          });
          pagination_init(result["length"]);
        } else
          $("#search_result .table tbody").append(
            '<tr><td colspan="11" class="text-center">No Data</td></tr>'
          );
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      $(".circle-loader").hide();
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}
////////////////////////////////////////////// Pagination-Javascript //////////////////////////////////////////////////
function pagination_init(len) {
  $("#pagination").show();
  $("#page_button").empty();
  $("#page_button").append(
    '<li class="page-item"><a class="page-link" id="page-first" href="javascript:void(0);"><<</a></li>'
  );
  $("#page_button").append(
    '<li class="page-item"><a class="page-link" id="page-prev" href="javascript:void(0);"><</a></li>'
  );
  page_len = Math.floor((len - 1) / 10) + 1;
  var start = 0;
  if (page_num - start >= 2) start = page_num - 2;
  if (start + 5 >= page_len) start = Math.max(page_len - 5, 0);

  var end = Math.min(start + 5, page_len);
  for (i = start; i < end; i++) {
    if (i == page_num)
      $("#page_button").append(
        '<li class="page-item active"><a class="page-link page-num" href="javascript:void(0);" page=' +
          i +
          ">" +
          (i + 1) +
          "</a></li>"
      );
    else
      $("#page_button").append(
        '<li class="page-item"><a class="page-link page-num" href="javascript:void(0);" page=' +
          i +
          ">" +
          (i + 1) +
          "</a></li>"
      );
  }
  $("#page_button").append(
    '<li class="page-item"><a class="page-link" id="page-next" href="javascript:void(0);">></a></li>'
  );
  $("#page_button").append(
    '<li class="page-item"><a class="page-link" id="page-end" href="javascript:void(0);">>></a></li>'
  );
  $(".page-num").click(function () {
    if (page_num == $(this).attr("page")) return;
    page_num = $(this).attr("page");
    show_result(page_num);
  });
  $("#page-first").click(function () {
    if (page_num == 0) return;
    page_num = 0;
    show_result(page_num);
  });
  $("#page-end").click(function () {
    if (page_num == page_len - 1) return;
    page_num = page_len - 1;
    show_result(page_num);
  });
  $("#page-prev").click(function () {
    if (page_num == 0) return;
    page_num -= 1;
    show_result(page_num);
  });
  $("#page-next").click(function () {
    if (page_num == page_len - 1) return;
    page_num += 1;
    show_result(page_num);
  });
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////

function remove_product(product_id) {
  postData = {
    type: "remove",
    product_id: product_id,
  };
  $.ajax({
    url: "/cart",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    timeout: 180000, // sets timeout to 3 minutes
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        $('[onclick="remove_product(' + product_id + ')"]')
          .parents("td")
          .html(
            '<button type="button" class="btn btn-success" onclick="add_product(' +
              product_id +
              ')"><i class="mdi mdi-cart-plus cart-icon"></i></button></button>'
          );
        $(".count_product").text(result["data"]["count_product"]);
        $("#balance").text("Balance: " + result["data"]["balance"] + " $");
        showSuccessToast("Removed item from cart", "Success");
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

function add_product(product_id) {
  postData = {
    type: "add",
    product_id: product_id,
  };
  $.ajax({
    url: "/cart",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        if (result["data"]["over_balance"])
          showWarningToast(
            "You are getting out of balance. Please recharge your balance.",
            "Warning"
          );
        else {
          $('[onclick="add_product(' + product_id + ')"]')
            .parents("td")
            .html(
              '<button type="button" class="btn btn-warning" onclick="remove_product(' +
                product_id +
                ')"><i class="mdi mdi-cart-minus cart-icon"></i></button>'
            );
          $(".count_product").text(result["data"]["count_product"]);
          $("#balance").text("Balance: " + result["data"]["balance"] + " $");
          showSuccessToast("Add item to cart", "Success");
        }
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

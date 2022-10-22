jQuery(document).ready(function () {
  show_result();
});

function show_result(page = 0) {
  $("#search_result").hide();
  $(".circle-loader").show();
  $("#search_result .table tbody").empty();

  postData = {
    type: "get",
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
        $("#search_result").show();
        $(".circle-loader").hide();
        var product_list = result["data"];
        var len = product_list.length;
        console.log(product_list);
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
            appendHTML += "<td>" + each["First_name"] + "</td>";
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
            appendHTML +=
              '<td class="text-right"><button type="button" class="btn btn-success" onclick="check_and_finalize(' +
              each["id"] +
              ')">Check<br>&<br>Finalize</button></td>';
            appendHTML +=
              '<td class="text-center"><button type="button" class="btn btn-warning" onclick="remove_product(' +
              each["id"] +
              ')"><i class="mdi mdi-cart-minus cart-icon"></i></button></td>';
            appendHTML += "</tr>";
            $("#search_result .table tbody").append(appendHTML);
          });
        } else
          $("#search_result .table tbody").append(
            '<tr><td colspan="12" class="text-center">No Data</td></tr>'
          );
      } else if (state == "FAIL") {
        $("#search_result").show();
        $(".circle-loader").hide();
        showDangerToast(result["error"], "Failed");
      } else {
        $("#search_result").show();
        $(".circle-loader").hide();
        showDangerToast("Cause an unknown error.", "Failed");
      }
    },
    error: function (xhr, status, error) {
      $("#search_result").show();
      $(".circle-loader").hide();
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

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
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        $('[onclick="remove_product(' + product_id + ')"]')
          .parents("tr")
          .remove();
        $(".count_product").text(result["data"]["count_product"]);
        $("#balance").text("Balance: " + result["data"]["balance"] + " $");
        if (result["data"]["count_product"] == 0)
          $("#search_result .table tbody").append(
            '<tr><td colspan="12" class="text-center">No Data</td></tr>'
          );
        showSuccessToast("Removed item from cart", "Success");
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

function check_and_finalize(product_id) {
  var td_element = $(
    '[onclick="check_and_finalize(' + product_id + ')"]'
  ).parents("td");
  var btn_html =
    '<button type="button" class="btn btn-success" onclick="check_and_finalize(' +
    product_id +
    ')">Check<br>&<br>Finalize</button>';
  var loader_html = '<div class="circle-loader"></div>';
  td_element.html(loader_html);
  postData = {
    checker_id: $('input[name="checkerRadio"]:checked').val(),
    product_id: product_id,
  };
  $.ajax({
    url: "/check",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      td_element.html(btn_html);
      var state = result["state"];
      if (state == "Done") {
        td_element.parents("tr").remove();
        showSuccessToast("Phone Registered Successfully", "Success");
        $(".count_product").text(result["data"]["count_product"]);
        if (result["data"]["count_product"] == 0)
          $("#search_result .table tbody").append(
            '<tr><td colspan="12" class="text-center">No Data</td></tr>'
          );
      } else if (state == "Fail") {
        td_element.parents("tr").remove();
        showWarningToast(result["error"], "Failed");
        $(".count_product").text(result["data"]["count_product"]);
        $("#balance").text("Balance: " + result["data"]["balance"] + " $");
        if (result["data"]["count_product"] == 0)
          $("#search_result .table tbody").append(
            '<tr><td colspan="12" class="text-center">No Data</td></tr>'
          );
      }else if (state == "Over_balance")
        showWarningToast(
          "You are getting out of balance. Please recharge your balance.",
          "Warning"
        )
      else showDangerToast(result["error"], "Error");
    },
    error: function (xhr, status, error) {
      td_element.html(btn_html);
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

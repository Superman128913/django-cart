jQuery(document).ready(function () {
  $(".datepicker").datepicker({
    enableOnReadonly: true,
    todayHighlight: true,
    autoclose: true,
  });
  $("#search_result").hide();
  $(".circle-loader").hide();
});

function show_result() {
  $(".circle-loader").show();
  $("#search_result").hide();
  $("#search_result .table tbody").empty();
  postData = {
    supplier_id: $("#supplier").val(),
    from_date: $("#from_date").children("input").val(),
    to_date: $("#to_date").children("input").val(),
    PaidUnpaid: $('input[name="PaidUnpaid"]:checked').val(),
  };
  $.ajax({
    url: "",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        $(".circle-loader").hide();
        $("#search_result").show();
        var data = result["data"];
        tableData = data["tableData"];
        var len = tableData.length;
        if (len) {
          tableData.forEach(function (each) {
            var appendHTML = "";
            appendHTML += '<tr batch_id="' + each["batch_id"] + '">';
            appendHTML +=
              '<td class="text-center"><input type="checkbox" class="row-checkbox"></td>';
            appendHTML +=
              '<td class="text-center">' + each["batch_id"] + "</td>";
            appendHTML +=
              '<td class="text-left">' + each["batch_name"] + "</td>";
            appendHTML +=
              '<td class="text-left">' + each["supplier_name"] + "</td>";
            appendHTML += "<td>" + each["supplier_batch_share"] + " % </td>";
            if (each["total_sold"])
              appendHTML +=
                "<td>" +
                each["total_sold"] +
                '<br><a href="javascript: void(0);" class="show-record total-sold">Show Records</a></td>';
            else appendHTML += "<td>" + each["total_sold"] + "</td>";
            appendHTML += "<td>" + each["total_sold_price"] + " $ </td>";
            appendHTML += "<td>" + each["total_supplier_profit"] + " $ </td>";
            appendHTML += "<td>" + each["total_shop_profit"] + " $ </td>";
            if (each["total_refund"])
              appendHTML +=
                "<td>" +
                each["total_refund"] +
                '<br><a href="javascript: void(0);" class="show-record total-refund">Show Records</a></td>';
            else appendHTML += "<td>" + each["total_refund"] + "</td>";
            if (each["total_unsold"])
              appendHTML +=
                "<td>" +
                each["total_unsold"] +
                '<br><a href="javascript: void(0);" class="show-record total-unsold">Show Records</a></td>';
            else appendHTML += "<td>" + each["total_unsold"] + "</td>";
            appendHTML += "</tr>";
            $("#search_result .table tbody").append(appendHTML);
          });
        } else
          $("#search_result .table tbody").append(
            '<tr><td colspan="11" class="text-center">No Data</td></tr>'
          );
        $("#total_batches").text(data["total_batches"]);
        $("#total_supplier").text(data["total_supplier"]);
        $("#total_sold").text(data["total_sold"]);
        $("#total_sold_price").text(data["total_sold_price"]);
        $("#total_supplier_profit").text(data["total_supplier_profit"]);
        $("#total_shop_profit").text(data["total_shop_profit"]);
        $("#total_refund").text(data["total_refund"]);
        $("#total_unsold").text(data["total_unsold"]);
        all_check_define();
        show_records_define();
      } else if (state == "FAIL") {
        $(".circle-loader").hide();
        $("#search_result").show();
        showDangerToast(result["error"], "Failed");
      } else {
        $(".circle-loader").hide();
        $("#search_result").show();
        showDangerToast("Cause an unknown error.", "Failed");
      }
    },
    error: function (xhr, status, error) {
      $(".circle-loader").hide();
      $("#search_result").show();
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

function all_check_define() {
  $("#all_check").prop("checked", false);
  $("#all_check").change(function () {
    $(".row-checkbox").prop("checked", $(this).prop("checked"));
  });
}

function set_paid() {
  if ($('input[name="PaidUnpaid"]:checked').val() == "PAID") return;

  var batch_list = [];
  $(".row-checkbox:checked").each(function () {
    batch_list.push($(this).parents("tr").attr("batch_id"));
  });
  postData = {
    from_date: $("#from_date").children("input").val(),
    to_date: $("#to_date").children("input").val(),
    PaidUnpaid: $('input[name="PaidUnpaid"]:checked').val(),
    batch_list: batch_list,
  };
  $.ajax({
    url: "/set_paid",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        showSuccessToast(
          "Selected Batches SOLD Records seted as PAID ",
          "Success"
        );
        show_result();
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
      showDangerToast(xhr.status + " " + xhr.statusText, "Failed");
    },
  });
}

///////////////////////////////////////////////Show Records//////////////////////////////////////////////
var page_num = 0;
var page_len = 0;
var type = ""; // total-sold/total-refund/total-unsold
var batch_id = 0;

function show_records_define() {
  $(".show-record").click(function () {
    element = $(this);
    if (element.hasClass("total-sold")) type = "total-sold";
    else if (element.hasClass("total-refund")) type = "total-refund";
    else if (element.hasClass("total-unsold")) type = "total-unsold";
    batch_id = element.parents("tr").attr("batch_id");

    show_records();
  });
}

function show_records(page = 0) {
  $("#show_records_modal").modal("show");
  $("#show_records_modal .table tbody").empty();
  postData = {
    from_date: $("#from_date").children("input").val(),
    to_date: $("#to_date").children("input").val(),
    PaidUnpaid: $('input[name="PaidUnpaid"]:checked').val(),
    type: type,
    batch_id: batch_id,
    page: page,
  };
  $.ajax({
    url: "/show_records",
    type: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": $('meta[name="csrf-token"]').attr('content'),
    },
    data: postData,
    success: function (result) {
      var state = result["state"];
      if (state == "OK") {
        var product_list = result["data"];
        $("#records_num").text(result["length"] + " records found");
        console.log(product_list);
        page_num = page;
        var len = product_list.length;
        if (len) {
          product_list.forEach(function (each) {
            var appendHTML = "";
            appendHTML += "<tr>";
            appendHTML += '<td class="text-center">' + each["Phone"] + "</td>";
            appendHTML +=
              "<td>" +
              each["Exp_day"] +
              "/" +
              each["Exp_month"] +
              "/" +
              each["Exp_year"] +
              "<br>" +
              each["Puk_code"] +
              "<br>" +
              each["Price"] +
              "$</td>";
            appendHTML +=
              "<td>" +
              each["Areaf1"] +
              "<br>" +
              each["Areaf2"] +
              "<br>" +
              each["Areaf3"] +
              "<br>" +
              each["Areaf4"] +
              "</td>";
            appendHTML +=
              '<td class="text-center"><img src="static/assets/vendors/flag-icon-css/flags/4x3/' +
              each["Areaf6"] +
              '.svg" alt="' +
              each["Areaf6"] +
              '.svg"><br>' +
              each["Areaf5"] +
              "</td>";
            appendHTML +=
              "<td>" +
              each["Address"] +
              "<br>" +
              each["City"] +
              "<br>" +
              each["State"] +
              "<br>" +
              each["Zipcode"] +
              "</td>";
            appendHTML +=
              "<td>" +
              each["First_name"] +
              "<br>" +
              each["Last_name"] +
              "<br>(" +
              each["Gender"] +
              ")</td>";
            appendHTML +=
              "<td>" +
              each["Extra1"] +
              "<br>" +
              each["Extra2"] +
              "<br>" +
              each["Extra3"] +
              "<br>" +
              each["Extra4"] +
              "<br>" +
              each["Extra5"] +
              "</td>";
            var Batch_Publish_date = new Date(each["Batch_Publish_date"]);
            appendHTML +=
              "<td>" +
              each["Batch_id"] +
              "<br>" +
              each["Batch_Name"] +
              "<br>" +
              Batch_Publish_date.getDate().toString().padStart(2, "0") +
              "/" +
              (Batch_Publish_date.getMonth() + 1).toString().padStart(2, "0") +
              "/" +
              Batch_Publish_date.getFullYear() +
              "</td>";
            if (each["Sold_unsold"] == "SOLD") {
              var Sold_date = new Date(each["Sold_date"]);
              appendHTML +=
                "<td>" +
                each["Sold_unsold"] +
                "<br>" +
                Sold_date.getDate().toString().padStart(2, "0") +
                "/" +
                (Sold_date.getMonth() + 1).toString().padStart(2, "0") +
                "/" +
                Sold_date.getFullYear() +
                "<br>" +
                each["Supplier_payment_status"] +
                "</td>";
            } else appendHTML += "<td>" + each["Sold_unsold"] + "<br>" + each["Supplier_payment_status"] + "</td>";
            appendHTML += "</tr>";
            $("#show_records_modal .table tbody").append(appendHTML);
          });
          pagination_init(result["length"]);
        } else
          $("#show_records_modal .table tbody").append(
            '<tr><td colspan="9" class="text-center">No Data</td></tr>'
          );
      } else if (state == "FAIL") showDangerToast(result["error"], "Failed");
      else showDangerToast("Cause an unknown error.", "Failed");
    },
    error: function (xhr, status, error) {
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
    show_records(page_num);
  });
  $("#page-first").click(function () {
    if (page_num == 0) return;
    page_num = 0;
    show_records(page_num);
  });
  $("#page-end").click(function () {
    if (page_num == page_len - 1) return;
    page_num = page_len - 1;
    show_records(page_num);
  });
  $("#page-prev").click(function () {
    if (page_num == 0) return;
    page_num -= 1;
    show_records(page_num);
  });
  $("#page-next").click(function () {
    if (page_num == page_len - 1) return;
    page_num += 1;
    show_records(page_num);
  });
}
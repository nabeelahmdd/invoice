function dispatch_toast(code, message) {
  console.log(code, message, '===')
  var message_class =
    code == 0 ? "error" : code == 2 ? "toast warning" : "success";
  $('body').append(`
    <div class="toast-container bottom-notification">
      <div class="toast align-items-center text-white bg-${message_class} border-0 alert-dismissible fade show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">
            ${message}
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
      </div>
    </div>
  `);
  
  setTimeout(function () {
    $('body .bottom-notification').remove()
  }, 2000);

}


function ajax_calling(ajax_options, callback = undefined) {
    var ajax_opts = ajax_options || {};
    ajax_opts.url = ajax_opts.url || "/";
    ajax_opts.type = ajax_opts.type || "POST";
    ajax_opts.data = ajax_opts.data || {};
    var multiple = ajax_opts.multiple;
    $(".loader-overlay").css('display', 'flex');
  
    $.ajax({
      url: ajax_opts.url, // the endpoint
      type: ajax_opts.type, // http method
      dataType: "json",
      data: ajax_opts.data,
  
      // handle a successful response
      success: function (data) {
        
        if (multiple != true) {
          success = data.code == 0 ? false : true;
          if (success && data.redirect) {
            $(".loader-overlay").hide();
            if(data.msg){
              dispatch_toast(data.code, data.msg);
              setTimeout(function () {
                window.location.href = data.redirect;
              }, 2000);
            }else{
              window.location.href = data.redirect;
            }
            
          } else {
            
            dispatch_toast(data.code, data.msg);
            
            $(".loader-overlay").hide();
          }
        } else {
          $(".loader-overlay").hide();
        }
      },
  
      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        $(".loader-overlay").hide();
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      },
    });
  }
  

function dispatch_ajax(url, data, name = "", multiple = false) {
    var ajaxOptions = {
      url: url,
      type: "POST",
      data: data,
      multiple: multiple,
    };
  
    ajax_calling(ajaxOptions);
  }
  

  $(document).on("click", ".delete-modal", function () {
    var url = $(this).attr('url');
    var title = $(this).attr('title');
    $('#deleteModal').attr('url', url);
    $('#deleteModal').modal('show');
    
  })

  $(document).on("click", ".close-delete-modal", function () {
    $('#deleteModal').modal('hide');
  })

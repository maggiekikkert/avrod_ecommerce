var stripe = Stripe('pk_test_FAFu3glBDqdKrdvJNOiF94iZ00LEThelHv');
var button = document.getElementById('checkout-btn');

button.addEventListener('click', function() {
  stripe.redirectToCheckout({
    sessionId: session_id
  }).then(function (result) {
    console.log(result.error.message)
  });
});

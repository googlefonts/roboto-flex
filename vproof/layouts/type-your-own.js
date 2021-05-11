(function() {
"use strict";
VideoProof.registerLayout('type-your-own', {
	'init': function(proof) {
		proof.textContent = "Type your own";
		proof.setAttribute('contenteditable', '');
	},
	'deinit': function(proof) {
		proof.removeAttribute('contenteditable');
	}
});
})();

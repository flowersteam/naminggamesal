
from . import SensoryApparatus
from scipy.interpolate import interp1d


class HumanHueSA(SensoryApparatus):
	def __init__(self, env=None):
		SensoryApparatus.__init__(self)
		#Data obtained with WebPlotDigitizer
		self.points = [
					(-0.002879078694817655, 0.030447761194029855),
					(0.002879078694817669, 0.02918739635157546),
					(0.007677543186180413, 0.02779436152570481),
					(0.014395393474088289, 0.025406301824212274),
					(0.02399232245681382, 0.0221558872305141),
					(0.033589251439539336, 0.018175787728026534),
					(0.044145873320537446, 0.013996683250414595),
					(0.053742802303262935, 0.011210613598673307),
					(0.06238003838771593, 0.009286898839137643),
					(0.07389635316698655, 0.008225538971807632),
					(0.08829174664107485, 0.00915422885572139),
					(0.10460652591170823, 0.011144278606965173),
					(0.12284069097888677, 0.012072968490878938),
					(0.1362763915547025, 0.01101160862354892),
					(0.14587332053742802, 0.008822553897180764),
					(0.16602687140115163, 0.004908789386401324),
					(0.18905950095969287, 0.002653399668325042),
					(0.22552783109404995, 0.0006633499170812587),
					(0.2706333973128599, 0.0007296849087893853),
					(0.30038387715930903, 0.0025870646766169153),
					(0.32149712092130517, 0.005837479270315089),
					(0.3474088291746641, 0.008955223880597017),
					(0.3752399232245681, 0.011144278606965173),
					(0.3934740882917466, 0.012338308457711444),
					(0.4241842610364684, 0.012736318407960204),
					(0.4616122840690979, 0.0145273631840796),
					(0.47888675623800386, 0.013930348258706468),
					(0.5009596928982725, 0.011210613598673307),
					(0.5249520153550864, 0.0073631840796019865),
					(0.557581573896353, 0.004112769485903819),
					(0.5950095969289827, 0.0017910447761193965),
					(0.6429942418426103, 0.0007296849087893853),
					(0.6833013435700575, 0.0009950248756218916),
					(0.7418426103646832, 0.0028524046434494146),
					(0.7975047984644913, 0.006169154228855722),
					(0.8541266794625719, 0.010480928689883914),
					(0.9021113243761995, 0.01592039800995025),
					(0.946257197696737, 0.023018242122719735),
					(0.9827255278310939, 0.03210613598673301),
					(0.9980806142034547, 0.03688225538971808),
					(1.0019193857965452, 0.039270315091210616)
				]
		self.x = [p[0] for p in self.points]
		self.y = [p[1] for p in self.points]	

	def d_min(self, h):
		f = interp1d(self.x,self.y,kind='cubic')
		return f(h)



	def discriminable(self, input_sig1, input_sig2):
		if abs(input_sig1 - input_sig2) >= max(self.d_min(input_sig1),self.d_min(input_sig2)):
			return True
		else:
			return False

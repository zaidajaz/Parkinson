

class park_functions:

	def get_algo_list():
		choices_algo_dict = {}

		algo_choices  = models.AlgoList.objects.all();
		for algo in algo_choices:
			choices_algo_dict[algo.algo_name] = algo.algo_display_name

		return choices_algo_dict
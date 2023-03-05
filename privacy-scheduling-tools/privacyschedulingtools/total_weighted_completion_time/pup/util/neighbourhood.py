import copy
from collections import defaultdict
from random import sample

class NeighborhoodGenerator:
    basic_nbh_cache = {}

    def __init__(self, max_size_per_depth=None):
        self.max_size_per_depth = max_size_per_depth

    def __basic_exact_swap_neighbourhood(self, number_of_jobs, max_swaps):
        if (number_of_jobs, max_swaps) in self.basic_nbh_cache.keys():
            return self.basic_nbh_cache[(number_of_jobs, max_swaps)]

        neighbourhood = {tuple(range(number_of_jobs)): 1}

        swaps = 1
        while swaps <= max_swaps:
            new_neighbourhood = defaultdict(int)
            for schedule_order in neighbourhood.keys():
                so_list = list(schedule_order)
                for i in range(0, len(so_list) - 1):
                    if(so_list[i] < so_list[i+1]):
                        neighbour_so_list = copy.deepcopy(so_list)
                        neighbour_so_list[i], neighbour_so_list[i+1] = so_list[i+1], so_list[i]
                        new_neighbourhood[tuple(neighbour_so_list)] += neighbourhood[schedule_order]
            swaps += 1
            neighbourhood = new_neighbourhood \
                if (not self.max_size_per_depth) or len(new_neighbourhood) < self.max_size_per_depth \
                else dict(sample(list(new_neighbourhood.items()), self.max_size_per_depth))

        self.basic_nbh_cache[(number_of_jobs, max_swaps)] = neighbourhood
        return neighbourhood

    def __translate_neighbourhood(self, original_schedule_order, basic_neighbourhood):
        translated_neighbourhood = {}
        for basic_schedule_order, count in basic_neighbourhood.items():
            translated_schedule_order = [original_schedule_order[i] for i in basic_schedule_order]
            translated_neighbourhood[tuple(translated_schedule_order)] = count
        return translated_neighbourhood


    def exact_swap_neighbourhood(self, original_schedule_order:list, swaps):
        '''
        Takes a schedule order and produces all permutations that are reachable
        with the given number of swaps from the original order.
        A swap is the exchange of two neighbouring elements of the list.
        Since the same state can be reached by different successions of swaps, each permutation can occur
        several times in the result, which is expressed by the dictionary values.
        :param original_schedule_order: a list representing the order of a schedule
        :param swaps: the number of swaps to be carried out
        :return: a dictionary of the form (permutation) -> number of occurences
        '''

        basic_nbh = self.__basic_exact_swap_neighbourhood(len(original_schedule_order), swaps)
        return self.__translate_neighbourhood(original_schedule_order, basic_nbh)


def main():
    jobs = list('abcde12345')
    nbh_generator = NeighborhoodGenerator()
    for swaps in range(1,10):
        neighbourhood = nbh_generator.exact_swap_neighbourhood(jobs, swaps)
        print(neighbourhood)
        print(len(neighbourhood))
        print(sum(neighbourhood.values()))

if __name__ == "__main__":
    main()

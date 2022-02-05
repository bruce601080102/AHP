import numpy as np


class AHPWeight:
    def __init__(self, ahp_weight) ->{"str": int}:
        self.ahp_weight = ahp_weight
        self.weight_list = None
        
    def ahp_evaluate(self):
        A_arr = self.algorithm_ahp_scale(self.weight_list)
        RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
        # 矩阵
        A = np.array(A_arr)

        a_sum0 = A.sum(axis=0)
        B = A / a_sum0  
        b_sum = B.sum(axis=1)

        W = b_sum.sum()
        w_arr = []
        for w in b_sum:
            w_arr.append(w/W)


        AW = []
        for a in A :
            aa = a * w_arr
            AW.append(aa.sum())

        result = np.array(AW) / np.array(w_arr)

        row = result.shape[0]
        Max = result.sum()/row

        CI = (Max - row) / (row - 1)
        # print('CI: %s' % CI)

        CR = CI / RI_dict[row]
        # print('CR: %s' % CR)
        return {"CI":CI, "CR":CR}

    def algorithm_ahp_scale(self, list_scale):
        def reciprocal(num):
            return [1. / np.array(abs(num))]

        dict_distance = {}
        # list_scale = [1, 2, -3, -4]
        list_array = []
        list_A_arr = []
        for i in list_scale:
            if i < 1:
                list_array.append(reciprocal(i)[0])
            else:
                list_array.append(i)
        # print(list_array)
        list_A_arr.append(list_array)

        for y in range(len(list_scale)):
            if y == 0:
                dict_distance[y] = list_array
            else:
                one_list = []
                for x in range(len(list_scale)):
                    # ====================正級距======================
                    if x == 0:
                        record = reciprocal(list_array[y])[0]
                        one_list.append(record)

                    if x != 0 and list_scale[y] > list_scale[x] and list_scale[x] > 0 and list_scale[y] > 0:
                        one_list.append(list_scale[x] / list_scale[y])
                    elif x != 0 and list_scale[y] == list_scale[x]:
                        one_list.append(1)
                    elif x != 0 and list_scale[y] < list_scale[x] and list_scale[y] > 0:
                        one_list.append(list_array[x] / list_array[y])
                    # y是正的，比較級距是負的
                    elif x != 0 and list_scale[y] > list_scale[x] and list_scale[x] < 0 and list_scale[y] > 0:
                        one_list.append(1 / (list_scale[y] - list_scale[x] + 1))

                    # ====================負級距======================
                    elif x != 0 and list_scale[y] > list_scale[x] and list_scale[y] < 0:
                        one_list.append((1 / list_scale[x]) / (1 / list_scale[y]))

                    elif x != 0 and list_scale[y] < list_scale[x] and list_scale[x] < 0 and list_scale[y] < 0:
                        one_list.append((1 / list_scale[x]) / (1 / list_scale[y]))

                    elif x != 0 and list_scale[y] < list_scale[x] and list_scale[x] > 0 and list_scale[y] < 0:
                        one_list.append(list_scale[x] - list_scale[y] + 1)

                list_A_arr.append(one_list)
        return list_A_arr

    def algorithm_ahp(self, A_arr):
        # 矩阵
        A = np.array(A_arr)
        a_sum0 = A.sum(axis=0)
        B = A / a_sum0
        b_sum = B.sum(axis=1)
        W = b_sum.sum()
        w_arr = []
        for w in b_sum:
            w_arr.append(w / W)
        return w_arr

    def output_weight(self):
        
        model_list, weight_list = list(self.ahp_weight.keys()), list(self.ahp_weight.values())
        idx = weight_list.index(1)

        weight_list[idx], weight_list[0] = weight_list[0], weight_list[idx]
        model_list[idx], model_list[0] = model_list[0], model_list[idx]
        ahp_weight = dict(zip(model_list, weight_list))
        
        
        list_scale = self.algorithm_ahp(self.algorithm_ahp_scale(weight_list))
        self.weight_list = weight_list
        for i, (k, _) in enumerate(ahp_weight.items()):
            ahp_weight[k] = round(list_scale[i], 6)
        return ahp_weight


def main():
    ahp_weight = {
        "test1": 1.6,
        "test2": 2.7,
        "test3": 1,
        "test4": 4,
        "test5": 4,
        "test6": 4,
        "test7": 2,
        "test8": 1.2
    }

    ahpw = AHPWeight(ahp_weight)
    dict_weight = ahpw.output_weight()
    print("AHP Weight:", dict_weight)
    print("AHP evaluate:", ahpw.ahp_evaluate())


if __name__ == '__main__':
    main()
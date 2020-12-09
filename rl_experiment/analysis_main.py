import pickle

# # 读取
with open('test_data.pickle', 'rb') as f:
    data = pickle.load(f)

'''
'''
for key, val in data.items():
    print(key)
    for s_key, s_val in val.items():
        print(s_key)
        for ss_key, ss_val in s_val.items():
            print(ss_key)
            print(ss_val)

'''
'''
f.close()
# import numpy as np
# import pandas as pd
# import seaborn as sns
# from scipy import stats
# import matplotlib as mpl
# import matplotlib.pyplot as plt

# sns.set(style="ticks")
# np.random.seed(sum(map(ord, "axis_grids")))

# tips = sns.load_dataset("tips")

# print(tips)
# g = sns.FacetGrid(tips, col="time")
# g.map(plt.hist, "tip");

# plt.show()

import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import codecs

sns.set(style="ticks")
np.random.seed(sum(map(ord, "axis_grids")))

type = pd.read_csv("Datasets.csv", encoding = 'utf8')
type = pd.Series(type["Type"], dtype="category")
print(type.count())

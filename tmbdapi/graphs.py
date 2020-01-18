import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import warnings

warnings.filterwarnings("ignore")

final_data = os.path.join("Results","tmbd_data_final.csv")
oscar_data = os.path.join("Data","data_csv.csv")
best_pictures = os.path.join("Results","TMBD_Data_best_picture.csv")

df1 = pd.read_csv(final_data)
df2 = pd.read_csv(oscar_data)
df3 = pd.read_csv(best_pictures)


def sum_of_releases():

    final_data = os.path.join("Results/tmbd_data_final.csv")
    df1 = pd.read_csv(final_data)
    df1["month"] = pd.to_datetime(df1["month"], format="%Y-%m")
    df1["year"] = df1["month"].dt.year
    release_df = (
        df1.groupby("year")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Sum of Releases")
    )
    release_df
    release_df.columns
    release_df.sort_values("year", inplace=True)
    release_df
    x = release_df["year"]
    y = release_df["Sum of Releases"]
    plt.figure(figsize=(15, 10))
    plt.title("Total Movie Releases by Year")
    plt.xlabel("Year")
    plt.ylabel("Movie Count")
    plt.bar(x, y)
    plt.grid()
    plt.savefig("Sum_of_Releases")
    return plt.show()



def tmbd_1980_profit():
    
    tmbd_1980 = os.path.join("Results/TMBD_data_post_1980.csv")
    df4 = pd.read_csv(tmbd_1980)
    df4["release_date"] = pd.to_datetime(df4["release_date"])
    df4["release_month"] = df4["release_date"].dt.month
    x = df4.groupby(["release_month"])["CPIAdjProfit"].mean()
    tmbd_1980_profit = pd.DataFrame(x)
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    tmbd_1980_profit.plot(kind="bar", ax=ax, color="purple")
    ax.set_xlabel(xlabel="Release Month", fontsize=12)
    ax.tick_params(axis="both", which="major", labelsize=10)
    plt.title("Movie Profit by Release Month", fontsize=12)
    plt.ylabel("Profit (CPI adjusted)", fontsize=12)
    formatter = ticker.FormatStrFormatter("$%1.2f")
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig("profit_release_month")
    return plt.show()


def bp_by_month():

    N = 12
    win_count = [0, 0, 0, 0, 4, 1, 1, 1, 4, 6, 6, 10]
    nom_count = [0, 5, 6, 0, 6, 7, 11, 10, 23, 18, 22, 58]
    ind = np.arange(N)
    plt.figure(figsize=(15, 10))
    width = 0.3
    plt.bar(ind, win_count, width, label="Winners", color="royalblue")
    plt.bar(ind + width, nom_count, width, label="Nominees", color="purple")
    plt.ylabel("Oscar Nomination Count")
    plt.title("Oscar Nominations for 'Best Picture'")
    plt.xticks(
        ind + width / 2,
        (
            "Jan",
            "Feb",
            "March",
            "April",
            "May",
            "June",
            "July",
            "Aug",
            "Sept",
            "Oct",
            "Nov",
            "Dec",
        ),
    )
    plt.legend(loc="best")
    plt.savefig("bp_by_month")
    return plt.show()


def bestpic_vote():
    
    ax = df3.boxplot(figsize=(10,6), column = ['vote_average'], by='Best_Picture', vert=False)
    df3.boxplot
    ax.set_title("Critic Vote on Best Picture", fontsize=12)
    ax.set_xlabel("Vote Average", fontsize=12)
    ax.set_ylabel("Oscar 'Best Picture' Result", )
    plt.subplots_adjust(left=0.25)
    plt.savefig("bp_vote")
    return plt.show()


# def profit_budget():
#     final_data = os.path.join("Results/tmbd_data_final.csv")
#     df1 = pd.read_csv(final_data)
#     ax = df1.plot.scatter(figsize=(12,8), x="CPIAdjBudget", y="CPIAdjProfit")
#     ax.set_xlim([0,600000000])
#     formatter = ticker.FormatStrFormatter("$%1.2f")
#     ax.yaxis.set_major_formatter(formatter)
#     ax.xaxis.set_major_formatter(formatter)
#     return plt.show()


# def budget_votes():

#     final_data = os.path.join("Results/tmbd_data_final.csv")
#     df1 = pd.read_csv(final_data)
#     df1["month"] = pd.to_datetime(df1["month"], format="%Y-%m")
#     df1["year"] = df1["month"].dt.year
#     x = df1.groupby(["vote_average"])["CPIAdjBudget"].median()
#     lang_budg = pd.DataFrame(x)
#     fig, ax = plt.subplots(1, 1, figsize=(15, 10))
#     plt.title("Movie Budget by Vote Count", fontsize=12)
#     ax.set_xlabel(xlabel="Vote Average", fontsize=12)
#     ax.tick_params(axis="both", which="major", labelsize=13)
#     plt.ylabel("Budget (CPI Adjusted)")
#     formatter = ticker.FormatStrFormatter("$%1.2f")
#     ax.yaxis.set_major_formatter(formatter)
#     return lang_budg.plot(kind="bar", ax=ax)

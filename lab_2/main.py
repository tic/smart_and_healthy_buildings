
def main():
    from pandas import read_csv
    df = read_csv('data.csv')

    df = df.drop('username', axis=1)
    df = df.drop('rps', axis=1)
    print(df)


    import seaborn as sns
    import matplotlib.pyplot as plt




    plt.show()
    # plot = sns.catplot(
    #     x="sesame",
    #     kind="count",
    #     data=df,
    #     palette="pastel"
    # )
    # plot.set(
    #     xlabel="Favorite Sesame Street Character",
    #     ylabel="Number of Students"
    # )
    # plt.show()

if __name__ == '__main__':
    main()

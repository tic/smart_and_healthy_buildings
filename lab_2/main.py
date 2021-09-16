
def main():
    from pandas import read_csv
    df = read_csv('data.csv')
    print(df)

    import seaborn as sns
    import matplotlib.pyplot as plt
    plot = sns.catplot(
        x="sesame",
        kind="count",
        data=df,
        palette="pastel"
    )
    plot.set(
        xlabel="Favorite Sesame Street Character",
        ylabel="Number of Students"
    )
    plt.show()

if __name__ == '__main__':
    main()

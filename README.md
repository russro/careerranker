# careerranker uses the elo rating system to score and rank your life choices.

Life choices are string combinations of 'locations', career 'types', and job 'titles'. These elements can be edited within the ```rank.py``` file.

If you want rank your own decisions, do the following:
1. Edit the elements at the top of ```rank.py```
2. Delete ```elos.json```
3. Keep ```choice_data.csv``` but clear its contents
4. Run ```python3 rank.py``` in the terminal

```choice_data.csv``` keeps a record of the choices you make, so you can can perform subsequent data analysis on which features are most predictive of the choice you make.

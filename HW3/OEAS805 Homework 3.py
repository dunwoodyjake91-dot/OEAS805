# %% [markdown]
# # Jacob D Homework 3 Machine Learning Regression

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
# More imports than are needed, copied from our practice notebooks

# %%
data_path = Path("CBP_TWQM_MAIN_WQ_2021_2026_surface.csv")
wq = pd.read_csv(data_path)
#print(wq.columns.tolist())
#print(wq["Parameter"].value_counts())

# %% [markdown]
# ## Target Variable Selection
#
# I chose chlorophyll-a (CHLA) as my target variable. CHLA is an
# indicator of phytoplankton biomass and is an important measure of water
# quality.

# I will use dissolved inorganic nitrogen (DIN) & total phosphorus (TP)
# as my predictor variables. These nutrients support phytoplankton growth, so
# they may help explain changes in CHLA. I am keeping my predictor
# list short to make the models easier to interpret.


# %%
model_data = wq.pivot_table(
    index=["FieldActivityId", "SampleDate"],
    columns="Parameter",
    values="MeasureValue",
    aggfunc="mean")[["DIN", "TP", "CHLA"]].dropna() #Avg any repeated measurmeants
# Check reshape and table print out
#print(model_data.head())
#print(f"Complete sampling events: {len(model_data)}")


# %% Separate predictor data from the target to be predicted 
X =model_data[["DIN", "TP"]]  # Model inputs nitrogen & phosphorus
y = model_data["CHLA"]         # Model output chla

# Show the number of rows and columns in each
#print("Predictors (rows, columns):", X.shape)
#print("Target (rows, values):", y.shape)


# %% Split data into training & testing groups

# Put sampling events in date order
model_data = model_data.sort_index(level="SampleDate")

# Recreate x & y in that same date order
X = model_data[["DIN", "TP"]]  # Predictors
y = model_data["CHLA"]         # CHLA values to predict

# Use the first 80% of events to train and the last 20% to test
split_point = int(len(model_data) * 0.8)

X_train = X.iloc[:split_point]
X_test = X.iloc[split_point:]
y_train = y.iloc[:split_point]
y_test = y.iloc[split_point:]

#print("Training events:", len(X_train))
#4print("Testing events:", len(X_test))


# %% Model 1 MLR

linear_model = LinearRegression()
# Let the model learn the relationship between DIN, TP, and CHLA
linear_model.fit(X_train, y_train)

# Use the trained model to predict CHLA 
linear_predictions = linear_model.predict(X_test)
print("Linear regression predictions:", linear_predictions)

# %% Plot the linear regression results

# Calculate how well predictions match the actual CHLA values
linear_r2 = r2_score(y_test, linear_predictions)

# Plot actual values against the models predictions
plt.figure(figsize=(6, 5))
plt.scatter(
    y_test, linear_predictions,
    edgecolor="black",
    label="Test predictions")

# This line shows where predictions would fall if they were 1-1
plot_min = min(y_test.min(), linear_predictions.min())
plot_max = max(y_test.max(), linear_predictions.max())
plt.plot(
    [plot_min, plot_max], [plot_min, plot_max],
    "r--",
    label="Perfect prediction")
plt.xlabel("Actual chlorophyll-a (CHLA)")
plt.ylabel("Predicted chlorophyll-a (CHLA)")
plt.title(f"Linear Regression Actual vs Predicted\nR² = {linear_r2:.2f}")
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Linear Regression Results
#
# Figure 1 compares measured CHLA with the linear
# regression model's predictions for the 9 test groups. The red dashed line
# shows where points would fall if predictions were exact.
#
# The test set R^2 is 0.59. Most points fall below the dashed line, indicating
# that the model often underpredicts CHLA. This is even more evident for the
# highest measured value which the model predicts way lower than the other points. 
# The model uses only DIN and TP as predictors. Other factors may also affect
# CHLA, so these two variables may not explain all the variation.



# %% Model 2 K Nearest Neighbors (KNN)

# Scale DIN and TP so their measurement ranges are comparable
knn_model = Pipeline([("scale", StandardScaler()),
    # Average CHLA from the 5 closest training events
    ("knn", KNeighborsRegressor(n_neighbors=5))])

# Learn from the training events, then predict CHLA for the test events
knn_model.fit(X_train, y_train)
knn_predictions = knn_model.predict(X_test)

# Calculate R2 using all 9 test events
knn_r2 =r2_score(y_test, knn_predictions)

# Set  figure range to include actual values & predictions
plot_min = min(y_test.min(), knn_predictions.min())
plot_max = max(y_test.max(), knn_predictions.max())

# Compare actual CHLA with KNN predictions
plt.figure(figsize=(6, 5))
plt.scatter(y_test, knn_predictions,edgecolor="black", label="Test predictions")

# Points on this line would be perfect predictions
plt.plot([plot_min, plot_max], [plot_min, plot_max],"r--", label="Perfect prediction")

plt.xlabel("Actual chlorophyll-a (CHLA)")
plt.ylabel("Predicted chlorophyll-a (CHLA)")
plt.title(f"KNN: Actual vs Predicted\nR² = {knn_r2:.2f}")
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## KNN Results
#
# I used 5 neighbors, so each prediction is based on the average CHLA value
# from the five most similar training events. With 33 training events, this
# provides a small neighbors without relying on only one event or averaging
# across most of the training data. 
# The test data R2 is 0.24. The plot shows that KNN underpredicts the higher
# CHLA values, including the highest test observation. Appears worse than MLR



# %% Fit & plot the MLP regression model

# Scale DIN and TP before fitting the neural network.
# One small hidden layer keeps the model simple for our limited training data.
mlp_model = Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPRegressor(hidden_layer_sizes=(5,),solver="lbfgs",alpha=0.01,max_iter=5000,random_state=42))])
mlp_model.fit(X_train, y_train)
mlp_predictions = mlp_model.predict(X_test)

# Compare predictions with the actual test values.
mlp_r2 = r2_score(y_test, mlp_predictions)

plt.figure(figsize=(6, 5))
plt.scatter(y_test, mlp_predictions, edgecolor="black",
            label="Test predictions")

# The dashed line shows where predictions would equal actual values.
plot_min = min(y_test.min(), mlp_predictions.min())
plot_max = max(y_test.max(), mlp_predictions.max())
plt.plot([plot_min, plot_max], [plot_min, plot_max], "r--",
         label="Perfect prediction")

plt.xlabel("Actual chlorophyll-a (CHLA)")
plt.ylabel("Predicted chlorophyll-a (CHLA)")
plt.title(f"MLP Regression Actual vs Predicted\nR² = {mlp_r2:.2f}")
plt.legend()
plt.tight_layout()
plt.show()


# %% [markdown]
# ## MLP Results
#
# I used one hidden layer with 5 nodes to keep the network small for this
# dataset (And I still don't fully get it). The inputs were scaled because neural networks can be affected by
# differences in each predictor scales. I used regularization (alpha=0.01) to help
# limit any overfitting.
#
# The MLP test dat R2 is 0.61, slightly higher than the linear regression
# result. It still underpredicts the highest CHLA value. Adding other relevant
# predictors, such as water temperature and water clarity may improve CHLA predictions.


# %% [markdown]
# ## Model Comparison
#
# The MLP had the highest test data R2 (0.61), just above Linear Regression
# (0.59). KNN had the lowest R2 (0.24). All three models underpredicted the
# highest CHLA value. This suggests that DIN and TP alone do not capture all
# the factors affecting CHLA. As said above having water temp or light intensity 
# would likely provide better predictions 
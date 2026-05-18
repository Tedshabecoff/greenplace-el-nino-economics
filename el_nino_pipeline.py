{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e0668266-82f2-4c08-81b7-a33144fcbe6a",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'scipy'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[1], line 23\u001b[0m\n\u001b[1;32m     21\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mmatplotlib\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mticker\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m FuncFormatter\n\u001b[1;32m     22\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mmatplotlib\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mgridspec\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mgridspec\u001b[39;00m\n\u001b[0;32m---> 23\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mscipy\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m stats\n\u001b[1;32m     24\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mwarnings\u001b[39;00m\n\u001b[1;32m     25\u001b[0m warnings\u001b[38;5;241m.\u001b[39mfilterwarnings(\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mignore\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'scipy'"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "El Niño Economics Pipeline — The Green Place, June 2026\n",
    "Data Spotlight: \"Every Degree of El Niño Costs This Much\"\n",
    "\n",
    "Data Sources:\n",
    "- ONI Index: NOAA CPC (https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt)\n",
    "- Economic costs: Callahan & Mankin (2023) Science doi:10.1126/science.adf2983\n",
    "                  Chen et al. (2023) Nature Communications doi:10.1038/s41467-023-41551-9\n",
    "- 2026 forecast: NOAA CPC ENSO Diagnostic Discussion (May 14, 2026)\n",
    "- Supply chain: USGS, BBVA Research, ScienceDirect supply disruption study (2024)\n",
    "\n",
    "Author: The Green Place / Ted Shabecoff\n",
    "\"\"\"\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib\n",
    "matplotlib.use('Agg')\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.patches as mpatches\n",
    "from matplotlib.ticker import FuncFormatter\n",
    "import matplotlib.gridspec as gridspec\n",
    "from scipy import stats\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e078223d-f342-4376-8652-cafb414642cf",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

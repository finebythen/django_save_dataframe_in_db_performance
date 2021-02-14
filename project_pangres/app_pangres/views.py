from django.shortcuts import render, redirect
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from django.utils.datastructures import MultiValueDictKeyError

from .models import UploadModelDemo


list_of_columns = [
        'first_name',
        'last_name',
        'age',
        'upload_id',
    ]

list_column_order = [
        'id',
        'first_name',
        'last_name',
        'age',
        'upload_id',
    ]


def convert_int_to_string_in_dataframe(df):
    df['age'] = df['age'].astype(str)
    df['upload_id'] = df['upload_id'].astype(str)

    return df


def main(request):

    try:
        if request.method == 'POST' and request.FILES['input-file']:
            try:
                # load database --> convert to dataframe
                qs_old = UploadModelDemo.objects.all()
                df_old = read_frame(qs_old)
                df_old.drop(['id'], axis=1, inplace=True)

                # load csv
                csv_file = request.FILES['input-file']

                # csv to dataframe --> filter for necessary columns
                df_new = pd.read_csv(csv_file, sep=";")
                df_new = df_new[df_new.columns[df_new.columns.isin(list_of_columns)]]

                # --> compare the two dataframe --> get separated dataframes in dictionary
                out = df_new.merge(df_old, how='outer', indicator='group')
                c = out.groupby("upload_id", sort=False).transform('nunique').gt(1).any(1)
                out['group'] = (np.select([out['group'].eq("both"), out['group'].ne("both") & c,
                                           out['group'].isin(['both', 'left_only']) & ~c],
                                          ['exists', 'updated', 'new']))

                d = dict(iter(out.groupby("group")))

                # --> extract dataframes from dictionary
                try:
                    df_updated = d['updated']
                except KeyError:
                    df_updated = pd.DataFrame()

                try:
                    df_new = d['new']
                except KeyError:
                    df_new = pd.DataFrame()

                # --> drop added 'group' column
                if df_updated.shape[0] > 0:
                    df_updated.drop(['group'], axis=1, inplace=True)

                if df_new.shape[0] > 0:
                    df_new.drop(['group'], axis=1, inplace=True)

                # --> convert dataframe to lists
                list_updated = df_updated.values.tolist()
                list_new = df_new.values.tolist()

                # --> remove doubled entrys from 'updated'-list
                list_drops = []
                for count, item in enumerate(list_updated):
                    if ((df_old['first_name'] == item[0]) & (df_old['last_name'] == item[1]) & (df_old['age'] == item[2]) & (df_old['upload_id'] == item[3])).any():
                        list_drops.append(count)

                # drop list items by position
                if len(list_drops) > 0:
                    for i in list_drops:
                        list_updated.pop(i)

                # --> save data with raw sql
                # --> SQL INSERT
                if len(list_new) > 0:
                    for i in list_new:
                        qs_insert = UploadModelDemo.objects.create(
                            first_name=i[0], last_name=i[1], age=i[2], upload_id=i[3]
                        )
                        qs_insert.save()

                # --> SQL UPDATE
                if len(list_updated) > 0:
                    for i in list_updated:
                        qs_update = UploadModelDemo.objects.filter(upload_id=i[3]).update(
                            first_name=i[0], last_name=i[1], age=i[2]
                        )

                return redirect("Main")

            except FileNotFoundError as e:
                print(e)
                pass
            except KeyError as e:
                print(e)
                pass
            except ValueError as e:
                print(e)
                pass
    except MultiValueDictKeyError as e:
        print(e)
        pass

    context = {}
    return render(request, 'app_pangres/main.html', context)

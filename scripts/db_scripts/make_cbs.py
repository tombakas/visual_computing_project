#!/usr/bin/env python3

import os
import json
import sqlite3
import argparse


DB_NAME = "./calls_20200323.db"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", default=".", help="Path to directory with batches"
    )
    args = parser.parse_args()
    return args


def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS cbs
       (id INTEGER PRIMARY KEY,
        region VARCHAR(60),
        city_name VARCHAR(10),
        a_inh_cat VARCHAR(6),
        a_inh REAL,
        a_00_14_cat VARCHAR(6),
        a_00_14 REAL,
        a_65_oo_cat VARCHAR(6),
        a_65_oo REAL,
        a_w_all_cat VARCHAR(6),
        a_w_all REAL,
        a_nw_all_cat VARCHAR(6),
        a_nw_all REAL,
        a_died_cat VARCHAR(6),
        a_died REAL,
        a_hh_cat VARCHAR(6),
        a_hh REAL,
        av_hh_size_cat VARCHAR(6),
        av_hh_size REAL,
        pop_den_km2_cat VARCHAR(6),
        pop_den_km2 REAL,
        av_prop_val_x005F_x1000_cat VARCHAR(6),
        av_prop_val_x1000 REAL,
        per_own_occ_cat VARCHAR(6),
        per_own_occ REAL,
        per_ren_hou_cat VARCHAR(6),
        per_ren_hou REAL,
        a_inc_rec_cat VARCHAR(6),
        a_inc_rec REAL,
        p_n_act_cat VARCHAR(6),
        p_n_act REAL,
        p_hh_usm_cat VARCHAR(6),
        p_hh_usm REAL,
        av_hou_theft_cat VARCHAR(6),
        av_hou_theft REAL,
        av_des_po_cat VARCHAR(6),
        av_des_po REAL,
        av_assault_cat VARCHAR(6),
        av_assault REAL,
        a_comp_cat VARCHAR(6),
        a_comp REAL)""")

    conn.commit()
    conn.close()


def process_entry(entry):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    command = """
       INSERT INTO cbs
       (region, city_name, a_inh_cat, a_inh, a_00_14_cat, a_00_14, a_65_oo_cat,
       a_65_oo, a_w_all_cat, a_w_all, a_nw_all_cat, a_nw_all, a_died_cat,
       a_died, a_hh_cat, a_hh, av_hh_size_cat, av_hh_size, pop_den_km2_cat,
       pop_den_km2, av_prop_val_x005F_x1000_cat, av_prop_val_x1000,
       per_own_occ_cat, per_own_occ, per_ren_hou_cat, per_ren_hou,
       a_inc_rec_cat, a_inc_rec, p_n_act_cat, p_n_act, p_hh_usm_cat, p_hh_usm,
       av_hou_theft_cat, av_hou_theft, av_des_po_cat, av_des_po,
       av_assault_cat, av_assault, a_comp_cat, a_comp)
       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       """

    print(command)
    print(entry)

    c.execute(command, entry)
    conn.commit()
    conn.close()


def main():
    create_db()

    with open("./cbs-data.csv") as f:
        f.readline() # Skip header
        for line in f:
            entries = line.split(";")
            row = []
            for entry in entries:
                if entry in ". ":
                    row.append(None)
                    continue
                try:
                    row.append(float(entry))
                except ValueError:
                    row.append(entry)

            process_entry(row)

if __name__ == "__main__":
    main()

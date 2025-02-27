"""
mpsim module.  Contains the ModpathSim class. Note that the user can access
the ModpathSim class as `flopy.modpath.ModpathSim`.

Additional information for this MODFLOW/MODPATH package can be found at the `Online
MODFLOW Guide
<https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/dis.html>`_.

"""
import numpy as np

from ..pakbase import Package
from ..utils import Util3d, import_optional_dependency

pd = import_optional_dependency(
    "pandas",
    error_message="writing particles is more effcient with pandas",
    errors="ignore",
)


class Modpath6Sim(Package):
    """
    MODPATH Simulation File Package Class.

    Parameters
    ----------
    model : model object
        The model object (of type :class:`flopy.modpath.mp.Modpath`) to which
        this package will be added.
    extension : string
        Filename extension (default is 'mpsim')


    Attributes
    ----------
    heading : str
        Text string written to top of package input file.

    Methods
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------

    >>> import flopy
    >>> m = flopy.modpath.Modpath6()
    >>> dis = flopy.modpath.Modpath6Sim(m)

    """

    def __init__(
        self,
        model,
        mp_name_file="mp.nam",
        mp_list_file="mp.list",
        option_flags=[1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1],
        ref_time=0,
        ref_time_per_stp=[0, 0, 1.0],
        stop_time=None,
        group_name=["group_1"],
        group_placement=[[1, 1, 1, 0, 1, 1]],
        release_times=[[1, 1]],
        group_region=[[1, 1, 1, 1, 1, 1]],
        mask_nlay=[1],
        mask_layer=[1],
        mask_1lay=[1],
        face_ct=[1],
        ifaces=[[6, 1, 1]],
        part_ct=[[1, 1, 1]],
        time_ct=1,
        release_time_incr=1,
        time_pts=[1],
        particle_cell_cnt=[[2, 2, 2]],
        cell_bd_ct=1,
        bud_loc=[[1, 1, 1, 1]],
        trace_id=1,
        stop_zone=1,
        zone=1,
        retard_fac=1.0,
        retard_fcCB=1.0,
        strt_file=None,
        extension="mpsim",
    ):
        # call base package constructor
        super().__init__(model, extension, "MPSIM", 32)
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper

        self.heading1 = "# MPSIM for Modpath, generated by Flopy."
        self.heading2 = "#"
        self.mp_name_file = f"{model.name}.mpnam"
        self.mp_list_file = f"{model.name}.mplst"
        options_list = [
            "SimulationType",
            "TrackingDirection",
            "WeakSinkOption",
            "WeakSourceOption",
            "ReferenceTimeOption",
            "StopOption",
            "ParticleGenerationOption",
            "TimePointOption",
            "BudgetOutputOption",
            "ZoneArrayOption",
            "RetardationOption",
            "AdvectiveObservationsOption",
        ]
        self.option_flags = option_flags
        options_dict = dict(list(zip(options_list, option_flags)))
        self.options_dict = options_dict
        self.endpoint_file = f"{model.name}.mpend"
        self.pathline_file = f"{model.name}.mppth"
        self.time_ser_file = f"{model.name}.mp.tim_ser"
        self.advobs_file = f"{model.name}.mp.advobs"
        self.ref_time = ref_time
        self.ref_time_per_stp = ref_time_per_stp
        self.stop_time = stop_time
        self.group_ct = len(group_name)
        self.group_name = group_name
        self.group_placement = group_placement
        self.release_times = release_times
        self.group_region = group_region
        self.mask_nlay = mask_nlay
        self.mask_layer = mask_layer
        self.mask_1lay = mask_1lay
        self.face_ct = face_ct
        self.ifaces = ifaces
        self.part_ct = part_ct
        self.strt_file = f"{model.name}.loc"
        if strt_file is not None:
            self.strt_file = strt_file
        self.time_ct = time_ct
        self.release_time_incr = release_time_incr
        self.time_pts = time_pts
        self.particle_cell_cnt = particle_cell_cnt
        self.cell_bd_ct = cell_bd_ct
        self.bud_loc = bud_loc
        self.trace_file = f"{model.name}.trace_file.txt"
        self.trace_id = trace_id
        self.stop_zone = stop_zone
        self.zone = Util3d(
            model,
            (nlay, nrow, ncol),
            np.int32,
            zone,
            name="zone",
            locat=self.unit_number[0],
        )
        self.retard_fac = retard_fac
        self.retard_fcCB = retard_fcCB

        # self.mask_nlay = Util3d(model,(nlay,nrow,ncol),np.int32,\
        # mask_nlay,name='mask_nlay',locat=self.unit_number[0])
        # self.mask_1lay = Util3d(model,(nlay,nrow,ncol),np.int32,\
        # mask_1lay,name='mask_1lay',locat=self.unit_number[0])
        # self.stop_zone = Util3d(model,(nlay,nrow,ncol),np.int32,\
        # stop_zone,name='stop_zone',locat=self.unit_number[0])
        # self.retard_fac = Util3d(model,(nlay,nrow,ncol),np.float32,\
        # retard_fac,name='retard_fac',locat=self.unit_number[0])
        # self.retard_fcCB = Util3d(model,(nlay,nrow,ncol),np.float32,\
        # retard_fcCB,name='retard_fcCB',locat=self.unit_number[0])

        self.parent.add_package(self)

    def check(self, f=None, verbose=True, level=1, checktype=None):
        """
        Check package data for common errors.

        Parameters
        ----------
        f : str or file handle
            String defining file name or file handle for summary file
            of check method output. If a sting is passed a file handle
            is created. If f is None, check method does not write
            results to a summary file. (default is None)
        verbose : bool
            Boolean flag used to determine if check method results are
            written to the screen
        level : int
            Check method analysis level. If level=0, summary checks are
            performed. If level=1, full checks are performed.

        Returns
        -------
        None

        Examples
        --------
        """
        chk = self._get_check(f, verbose, level, checktype)

        # MODPATH apparently produces no output if stoptime > last timepoint
        if (
            self.options_dict["StopOption"] == 3
            and self.options_dict["TimePointOption"] == 3
        ):
            if self.time_pts[-1] < self.stop_time:
                chk._add_to_summary(
                    type="Error",
                    value=self.stop_time,
                    desc="Stop time greater than last TimePoint",
                )
            else:
                chk.append_passed("Valid stop time")
            chk.summarize()
        return chk

    def write_file(self):
        """
        Write the package file

        Returns
        -------
        None

        """
        # item numbers and CamelCase variable names correspond to Modpath 6 documentation
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper

        f_sim = open(self.fn_path, "w")
        # item 0
        f_sim.write(f"#{self.heading1}\n#{self.heading2}\n")
        # item 1
        f_sim.write(f"{self.mp_name_file}\n")
        # item 2
        f_sim.write(f"{self.mp_list_file}\n")
        # item 3
        for i in range(12):
            f_sim.write(f"{self.option_flags[i]:4d}")
        f_sim.write("\n")

        # item 4
        f_sim.write(f"{self.endpoint_file}\n")
        # item 5
        if self.options_dict["SimulationType"] == 2:
            f_sim.write(f"{self.pathline_file}\n")
        # item 6
        if self.options_dict["SimulationType"] == 3:
            f_sim.write(f"{self.time_ser_file}\n")
        # item 7
        if (
            self.options_dict["AdvectiveObservationsOption"] == 2
            and self.option_dict["SimulationType"] == 3
        ):
            f_sim.write(f"{self.advobs_file}\n")

        # item 8
        if self.options_dict["ReferenceTimeOption"] == 1:
            f_sim.write(f"{self.ref_time:f}\n")
        # item 9
        if self.options_dict["ReferenceTimeOption"] == 2:
            Period, Step, TimeFraction = self.ref_time_per_stp
            f_sim.write(f"{Period + 1} {Step + 1} {TimeFraction:f}\n")

        # item 10
        if self.options_dict["StopOption"] == 3:
            f_sim.write(f"{self.stop_time:f}\n")

        if self.options_dict["ParticleGenerationOption"] == 1:
            # item 11
            f_sim.write(f"{self.group_ct}\n")
            for i in range(self.group_ct):
                # item 12
                f_sim.write(f"{self.group_name[i]}\n")
                # item 13
                (
                    Grid,
                    GridCellRegionOption,
                    PlacementOption,
                    ReleaseStartTime,
                    ReleaseOption,
                    CHeadOption,
                ) = self.group_placement[i]
                f_sim.write(
                    "{0:d} {1:d} {2:d} {3:f} {4:d} {5:d}\n".format(
                        Grid,
                        GridCellRegionOption,
                        PlacementOption,
                        ReleaseStartTime,
                        ReleaseOption,
                        CHeadOption,
                    )
                )
                # item 14
                if ReleaseOption == 2:
                    (
                        ReleasePeriodLength,
                        ReleaseEventCount,
                    ) = self.release_times[i]
                    f_sim.write(
                        f"{ReleasePeriodLength:f} {ReleaseEventCount}\n"
                    )
                # item 15
                if GridCellRegionOption == 1:
                    (
                        MinLayer,
                        MinRow,
                        MinColumn,
                        MaxLayer,
                        MaxRow,
                        MaxColumn,
                    ) = self.group_region[i]
                    f_sim.write(
                        "{0:d} {1:d} {2:d} {3:d} {4:d} {5:d}\n".format(
                            MinLayer + 1,
                            MinRow + 1,
                            MinColumn + 1,
                            MaxLayer + 1,
                            MaxRow + 1,
                            MaxColumn + 1,
                        )
                    )
                # item 16
                if GridCellRegionOption == 2:
                    f_sim.write(self.mask_nlay[i].get_file_entry())
                    # item 17
                if GridCellRegionOption == 3:
                    f_sim.write(f"{self.mask_layer[i]}\n")
                    # item 18
                    f_sim.write(self.mask_1lay[i].get_file_entry())
                # item 19 and 20
                if PlacementOption == 1:
                    f_sim.write(f"{self.face_ct[i]}\n")
                    # item 20
                    for j in range(self.face_ct[i]):
                        (
                            IFace,
                            ParticleRowCount,
                            ParticleColumnCount,
                        ) = self.ifaces[i][j]
                        f_sim.write(
                            f"{IFace} {ParticleRowCount} {ParticleColumnCount}\n"
                        )
                # item 21
                elif PlacementOption == 2:
                    (
                        ParticleLayerCount,
                        ParticleRowCount,
                        ParticleColumnCount,
                    ) = self.particle_cell_cnt[i]
                    f_sim.write(
                        "{0:d} {1:d} {2:d} \n".format(
                            ParticleLayerCount,
                            ParticleRowCount,
                            ParticleColumnCount,
                        )
                    )

        # item 22
        if self.options_dict["ParticleGenerationOption"] == 2:
            f_sim.write(f"{self.strt_file}\n")

        if self.options_dict["TimePointOption"] != 1:
            # item 23
            if (
                self.options_dict["TimePointOption"] == 2
                or self.options_dict["TimePointOption"] == 3
            ):
                f_sim.write(f"{self.time_ct}\n")
            # item 24
            if self.options_dict["TimePointOption"] == 2:
                f_sim.write(f"{self.release_time_incr:f}\n")
            # item 25
            if self.options_dict["TimePointOption"] == 3:
                for r in range(self.time_ct):
                    f_sim.write(f"{self.time_pts[r]:f}\n")

        if (
            self.options_dict["BudgetOutputOption"] != 1
            or self.options_dict["BudgetOutputOption"] != 2
        ):
            # item 26
            if self.options_dict["BudgetOutputOption"] == 3:
                f_sim.write(f"{self.cell_bd_ct}\n")
                # item 27
                for k in range(self.cell_bd_ct):
                    Grid, Layer, Row, Column = self.bud_loc[k]
                    f_sim.write(
                        f"{Grid} {Layer + 1} {Row + 1} {Column + 1} \n"
                    )
            if self.options_dict["BudgetOutputOption"] == 4:
                # item 28
                f_sim.write(f"{self.trace_file}\n")
                # item 29
                f_sim.write(f"{self.trace_id}\n")

        if self.options_dict["ZoneArrayOption"] != 1:
            # item 30
            f_sim.write(f"{self.stop_zone}\n")
            # item 31
            f_sim.write(self.zone.get_file_entry())

        if self.options_dict["RetardationOption"] != 1:
            # item 32
            f_sim.write(self.retard_fac.get_file_entry())
            # item 33
            f_sim.write(self.retard_fcCB.get_file_entry())

        f_sim.close()


class StartingLocationsFile(Package):
    """
    Class for working with MODPATH Starting Locations file for particles.

    Parameters
    ----------
    model : Modpath object
        The model object (of type :class:`flopy.modpath.mp.Modpath`) to which
        this package will be added.
    inputstyle : 1
        Input style described in MODPATH6 manual (currently only input style 1 is supported)
    extension : string
        Filename extension (default is 'loc')

    use_pandas: bool, if True and pandas is available use pandas to write the particle locations >2x speed
    """

    def __init__(
        self,
        model,
        inputstyle=1,
        extension="loc",
        verbose=False,
        use_pandas=True,
    ):
        super().__init__(model, extension, "LOC", 33)

        self.model = model
        self.use_pandas = use_pandas
        self.heading = (
            "# Starting locations file for Modpath, generated by Flopy."
        )
        self.input_style = inputstyle
        if inputstyle != 1:
            raise NotImplementedError
        self.data = self.get_empty_starting_locations_data(0)
        self.extension = extension

        # add to package list so location are written with other ModPath files
        self.parent.add_package(self)

    @staticmethod
    def get_dtypes():
        """
        Build numpy dtype for the MODPATH 6 starting locations file.
        """
        dtype = np.dtype(
            [
                ("particleid", int),
                ("particlegroup", int),
                ("initialgrid", int),
                ("k0", int),
                ("i0", int),
                ("j0", int),
                ("xloc0", np.float32),
                ("yloc0", np.float32),
                ("zloc0", np.float32),
                ("initialtime", np.float32),
                ("label", "|S40"),
                ("groupname", "|S16"),
            ]
        )
        return dtype

    @staticmethod
    def get_empty_starting_locations_data(
        npt=0, default_xloc0=0.5, default_yloc0=0.5, default_zloc0=0.0
    ):
        """get an empty recarray for particle starting location info.

        Parameters
        ----------
        npt : int
            Number of particles. Particles in array will be numbered consecutively from 1 to npt.

        """
        dtype = StartingLocationsFile.get_dtypes()
        d = np.zeros(npt, dtype=dtype)
        d = d.view(np.recarray)
        d["particleid"] = np.arange(1, npt + 1)
        d["particlegroup"] = 1
        d["initialgrid"] = 1
        d["xloc0"] = default_xloc0
        d["yloc0"] = default_yloc0
        d["zloc0"] = default_zloc0
        d["groupname"] = "group1"
        return d

    def write_file(self, data=None, float_format="{:.8f}"):
        if data is None:
            data = self.data
        if len(data) == 0:
            print("No data to write!")
            return
        data = data.copy()
        data["k0"] += 1
        data["i0"] += 1
        data["j0"] += 1
        if pd is not None and self.use_pandas and len(data) > 0:
            self._write_particle_data_with_pandas(data, float_format)
        else:
            self._write_wo_pandas(data, float_format)

    def _write_particle_data_with_pandas(self, data, float_format):
        """
        write particle data with pandas, more than twice as efficient
        :param data: particle data, pd.Dataframe or numpy record array with keys:
                          ['k0', 'i0', 'j0', 'groupname', 'particlegroup', 'xloc0', 'yloc0', 'zloc0',
                          'initialtime', 'label']
        :param save_group_mapper bool, if true, save a groupnumber to group name mapper as well.
        :return:
        """
        # convert float format string to pandas float format
        float_format = (
            float_format.replace("{", "").replace("}", "").replace(":", "%")
        )
        data = pd.DataFrame(data)
        if len(data) == 0:
            return
        # check if byte strings and decode
        if isinstance(data.label.iloc[0], (bytes, bytearray)):
            data.loc[:, "label"] = data.label.str.decode("UTF-8")
        if isinstance(data.groupname.iloc[0], (bytes, bytearray)):
            data.loc[:, "groupname"] = data.groupname.str.decode("UTF-8")

        # write loc file with pandas to save time
        # simple speed test writing particles with flopy and running model took 30 min, writing with pandas took __min
        loc_path = self.fn_path
        # write groups
        group_dict = dict(
            data[["particlegroup", "groupname"]].itertuples(False, None)
        )

        # writing group loc data
        groups = (
            data[["particlegroup", "groupname"]]
            .groupby("particlegroup")
            .count()
            .reset_index()
            .rename(columns={"groupname": "count"})
        )
        groups.loc[:, "groupname"] = groups.loc[:, "particlegroup"].replace(
            group_dict
        )
        group_count = len(groups.index)
        groups = pd.Series(
            groups[["groupname", "count"]].astype(str).values.flatten()
        )
        with open(loc_path, "w") as f:
            f.write("{}\n".format(self.heading))
            f.write("{:d}\n".format(self.input_style))
            f.write("{}\n".format(group_count))

        groups.to_csv(loc_path, sep=" ", index=False, header=False, mode="a")

        # write particle data
        print("writing loc particle data")
        data.drop("groupname", 1, inplace=True)
        data.to_csv(
            loc_path,
            sep=" ",
            header=False,
            index=False,
            mode="a",
            float_format=float_format,
        )

    def _write_wo_pandas(self, data, float_format):
        with open(self.fn_path, "w") as output:
            output.write(f"{self.heading}\n")
            output.write(f"{self.input_style}\n")
            groups = np.unique(data.groupname)
            ngroups = len(groups)
            output.write(f"{ngroups}\n")
            for g in groups:
                npt = len(data[data.groupname == g])
                output.write(f"{g.decode()}\n{npt}\n")
            txt = ""
            for p in data:
                txt += "{:d} {:d} {:d} {:d} {:d} {:d}".format(*list(p)[:6])
                fmtstr = " {0} {0} {0} {0} ".format(float_format)
                txt += fmtstr.format(*list(p)[6:10])
                txt += f"{p[10].decode()}\n"
            output.write(txt)

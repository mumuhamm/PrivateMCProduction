import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

_generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bsmm.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface-EvtGenInterface/Bs_Phimumugamma.dec'),
            list_forced_decays = cms.vstring('MyB_s0', 'Myanti-B_s0'),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CP5SettingsBlock,
    processParameters = cms.vstring(
        "SoftQCD:nonDiffractive = on",
        'PTFilter:filter = off',
        'PTFilter:quarkToFilter = 5',# bottom quark 
        'PTFilter:scaleToFilter = 1.0'
        #'TimeShower:pTmin = 3.0',  # Increased for soft emission handling
        #'SpaceShower:pTmin = 3.0',  # Matching minimum pT for space-like showers
        #'SpaceShower:rapidityOrder = off',  # Avoid too-soft emissions
        #'MultipartonInteractions:pTmin = 3.0',  # MPI pTmin to avoid low-pT interactions
        #'MultipartonInteractions:pT0Ref = 2.0',  # Adjust for stability
        #'PDF:pSet = LHAPDF6:NNPDF31_nnlo_as_0118',  # Use specific PDF set
        #'SpaceShower:pTminChgQ = 2.0',  # Minimum scale for charged parton emissions
        #'Variations:doVariations = on',
        #'HadronLevel:all = on'
    ),
    parameterSets = cms.vstring(
        'pythia8CommonSettings',
        'pythia8CP5Settings',
        'processParameters',
    )
)
)

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)

bfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(531)
)

decayfilter = cms.EDFilter("PythiaAllDauVFilter",
    moduleLabel = cms.untracked.InputTag("generator","unsmeared"),
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(531),
    DaughterIDs     = cms.untracked.vint32(333, 22),
    MinPt           = cms.untracked.vdouble(0,0),
    MinEta          = cms.untracked.vdouble(-2.5,-3),
    MaxEta          = cms.untracked.vdouble(2.5,3)
)
phifilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(13, -13),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MinPt = cms.untracked.vdouble(0,0),
    MotherID = cms.untracked.int32(531),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(333),
    verbose = cms.untracked.int32(1)
)


ProductionFilterSequence = cms.Sequence(generator*bfilter*decayfilter*phifilter)

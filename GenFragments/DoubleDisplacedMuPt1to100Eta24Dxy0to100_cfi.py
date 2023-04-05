import FWCore.ParameterSet.Config as cms

generator = cms.EDProducer("FlatRandomPtAndDxyGunProducer",
    PGunParameters = cms.PSet(
        MinPt = cms.double(1.0),
        MaxPt = cms.double(100.0),
        PartID = cms.vint32(13),
        MaxEta = cms.double(2.4),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-2.4),
        MinPhi = cms.double(-3.14159265359), ## in radians
        # Displacement parameters in mm
        LxyMax = cms.double(3000.0),#make sure most muons generated before Muon system, Gauss distribution
        LzMax = cms.double(5000.0),#make sure most muons generated before Muon system, Gauss distribution
        ConeRadius = cms.double(1000.0),
        ConeH = cms.double(3000.0),
        DistanceToAPEX = cms.double(2000.0),
        dxyMin = cms.double(0.0),
        dxyMax = cms.double(100.0)
    ),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts

    psethack = cms.string('double displaced mu pt 1-100 dxy 0-100'),
    AddAntiParticle = cms.bool(True),
    firstRun = cms.untracked.uint32(1)                           
)

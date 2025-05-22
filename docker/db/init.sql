-- Таблица для хранения изображений
CREATE TABLE IF NOT EXISTS images (
  id VARCHAR PRIMARY KEY,
  name VARCHAR NOT NULL,
  lat DOUBLE PRECISION NOT NULL,
  lon DOUBLE PRECISION NOT NULL,
  url VARCHAR NOT NULL
);

-- Примерные данные

INSERT INTO images (id, name, lat, lon, url) VALUES
  ('img001',  'Eiffel Tower',         48.8584,    2.2945,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/eiffel.jpg'),
  ('img002',  'Statue of Liberty',    40.6892,   -74.0445,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/liberty.jpg'),
  ('img003',  'Big Ben',              51.5007,   -0.1246,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/bigben.jpg'),
  ('img004',  'Colosseum',            41.8902,   12.4922,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/colosseum.jpg'),
  ('img005',  'Christ the Redeemer',  -22.9519,  -43.2105,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/redeemer.jpg'),
  ('img006',  'Great Wall (Mutianyu)',40.4319,  116.5704,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/greatwall.jpg'),
  ('img007',  'Sydney Opera House',   -33.8568,  151.2153,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/opera.jpg'),
  ('img008',  'Machu Picchu',         -13.1631,  -72.5450,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/machu.jpg'),
  ('img009',  'Taj Mahal',             27.1751,   78.0421,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/tajmahal.jpg'),
  ('img010',  'Christ Church',         52.2043,    0.1218,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/christchurch.jpg'),
  ('img011',  'Golden Gate Bridge',    37.8199,  -122.4783,   'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/goldengate.jpg'),
  ('img012',  'Mount Fuji',           35.3606,  138.7274,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/fuji.jpg'),
  ('img013',  'Stonehenge',            51.1789,   -1.8262,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/stonehenge.jpg'),
  ('img014',  'Petra',                 30.3285,   35.4444,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/petra.jpg'),
  ('img015',  'Angkor Wat',            13.4125,  103.8667,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/angkor.jpg'),
  ('img016',  'Pyramids of Giza',      29.9792,   31.1342,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/giza.jpg'),
  ('img017',  'Niagara Falls',         43.0962,   -79.0377,   'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/niagara.jpg'),
  ('img018',  'Burj Khalifa',          25.1972,   55.2744,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/burj.jpg'),
  ('img019',  'Christ the King',       -8.0958,  -34.8813,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/christking.jpg'),
  ('img020',  'Mount Kilimanjaro',     -3.0674,   37.3556,    'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/kili.jpg'),
  ('img021', 'Moscow Kremlin',       55.7520,   37.6175,      'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/kremlin.jpg'),
  ('img022', 'Hermitage Museum',      59.9398,   30.3146,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/hermitage.jpg'),
  ('img023', 'Lake Baikal',           53.5587,  108.1650,     'https://raw.githubusercontent.com/MesserMMP/Images/main/geoclip-images/baikal.jpg')
ON CONFLICT (id) DO NOTHING;

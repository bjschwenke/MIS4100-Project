-- Create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS `TestProductManagement`;


-- Use the database
USE `TestProductManagement`;


Drop table if exists `sales`;
Drop table if exists `orders`;
Drop table if exists `draftorders`;
Drop table if exists `inventory`;
Drop table if exists `running low`;
drop table if exists `salesdetails`;


CREATE TABLE Inventory (
    UPC BIGINT PRIMARY KEY,       -- Universal Product Code (Unique Identifier)
    VendorID INT NOT NULL,            -- Vendor ID (Assuming an integer ID)
    VendorCode VARCHAR(50),           -- Vendor-specific code
    UOM VARCHAR(10),                   -- Unit of Measure
    BaseCost DECIMAL(10,2),           -- Cost per unit
    CaseSize INT,                      -- Number of units per case
    Brand VARCHAR(100),                -- Brand Name
    Quantity INT,                       -- Stock Quantity
    Description TEXT,                   -- Product Description
    Size VARCHAR(20),                   -- Size of the item (e.g., "500ml")
    VolWeight DECIMAL(10,2),          -- Volume or weight
    Measure VARCHAR(10),               -- Measurement unit (e.g., "oz", "kg")
    SubDepartment VARCHAR(10),        -- Sub-category
    Deposit DECIMAL(10,2),             -- Deposit fee if applicable
    Scalable BOOLEAN,                   -- Whether the product is scalable
    Price DECIMAL(10,2),               -- Regular price
    SalePrice DECIMAL(10,2),          -- Discounted price
    DateReceived DATE                -- Date the inventory was received
);
Create table if not exists `sales`(
	`Date` date not null,
	`UPC` BIGINT not null,
	`Description` MEDIUMTEXT not null,
	`AMT` Decimal (10,2) not null,
	`Qty` int not null,
	`Wgt` Decimal (10,5) null
);
Create table if not exists `orders`(
	`Date` date not null,
	`Upc` BIGINT,
	`VendorCode` Int,
	`Cases` Int
);
Create table if not exists `draftorders`(
	`Date` date not null,
	`Upc` BIGINT,
	`VendorCode` Int,
	`Cases` Int
);
Create table if not exists `runninglow`(
	`Upc` bigint not null,
	`Qty` int not null,
	`Sub-Department` varchar(10),
	`VendorID` int not null
);

create table if not exists `salesdetails`(
	`Date` date not null,
	`UPC` BIGINT not null,
	`Description` MEDIUMTEXT not null,
	`AMT` Decimal (10,2) not null,
	`Qty` int not null,
	`Wgt` Decimal (10,5) null
);

INSERT INTO sales (Date, UPC, Description, AMT, Qty, Wgt)
VALUES
('2025-04-01', 123456789012, 'Organic Bananas', 5.99, 3, 2.34567),
('2025-04-01', 987654321098, 'Almond Milk - Unsweetened 1L', 3.49, 2, NULL),
('2025-04-02', 456789123456, 'Whole Wheat Bread - Loaf', 2.79, 1, NULL),
('2025-04-02', 321654987012, 'Chicken Breast - Boneless Skinless', 12.50, 2, 1.25000),
('2025-04-03', 654987321654, 'Frozen Mixed Berries 500g', 6.25, 1, 0.50000);

INSERT INTO salesdetails (Date, UPC, Description, AMT, Qty, Wgt)
VALUES
('2025-04-01', 123456789012, 'Organic Bananas', 5.99, 3, 2.34567),
('2025-04-01', 987654321098, 'Almond Milk - Unsweetened 1L', 3.49, 2, NULL),
('2025-04-02', 456789123456, 'Whole Wheat Bread - Loaf', 2.79, 1, NULL),
('2025-04-02', 321654987012, 'Chicken Breast - Boneless Skinless', 12.50, 2, 1.25000),
('2025-04-03', 654987321654, 'Frozen Mixed Berries 500g', 6.25, 1, 0.50000);

INSERT INTO runninglow (Upc, Qty, `Sub-Department`, VendorID)
VALUES
(100000000001, 5, 'PROD', 101),
(100000000002, 3, 'DAIRY', 102),
(100000000003, 2, 'BAKERY', 103),
(100000000004, 4, 'MEAT', 104),
(100000000005, 6, 'FROZEN', 105);

INSERT INTO Inventory (
    UPC, VendorID, VendorCode, UOM, BaseCost, CaseSize, Brand,
    Quantity, Description, Size, VolWeight, Measure, SubDepartment,
    Deposit, Scalable, Price, SalePrice, DateReceived
)
VALUES
(100000000001, 101, 'VEND101', 'EA', 0.89, 12, 'Dole',
 150, 'Organic Bananas', '1lb', 1.00, 'lb', 'PROD', 0.00, TRUE, 0.99, 0.89, '2025-04-01'),

(100000000002, 102, 'VEND102', 'EA', 2.35, 6, 'Silk',
 80, 'Almond Milk - Unsweetened 1L', '1L', 1.00, 'L', 'DAIRY', 0.10, FALSE, 2.99, 2.49, '2025-04-02'),

(100000000003, 103, 'VEND103', 'EA', 1.15, 10, 'Wonder',
 60, 'Whole Wheat Bread - Loaf', '500g', 0.50, 'g', 'BAKERY', 0.00, FALSE, 1.89, 1.59, '2025-04-02'),

(100000000004, 104, 'VEND104', 'EA', 5.50, 8, 'Tyson',
 40, 'Chicken Breast - Boneless Skinless', '1kg', 1.00, 'kg', 'MEAT', 0.00, TRUE, 7.99, 6.99, '2025-04-03'),

(100000000005, 105, 'VEND105', 'EA', 3.00, 12, 'Great Value',
 100, 'Frozen Mixed Berries 500g', '500g', 0.50, 'g', 'FROZEN', 0.00, FALSE, 4.49, 3.99, '2025-04-04');

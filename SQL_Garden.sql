USE [master]
GO
/****** Object:  Database [Garden]    Script Date: 6/24/2024 7:04:28 PM ******/
CREATE DATABASE [Garden]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Garden', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\Garden.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'Garden_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\Garden_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [Garden] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Garden].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Garden] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Garden] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Garden] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Garden] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Garden] SET ARITHABORT OFF 
GO
ALTER DATABASE [Garden] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [Garden] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Garden] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Garden] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Garden] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Garden] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Garden] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Garden] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Garden] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Garden] SET  ENABLE_BROKER 
GO
ALTER DATABASE [Garden] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Garden] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Garden] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Garden] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Garden] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Garden] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Garden] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Garden] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [Garden] SET  MULTI_USER 
GO
ALTER DATABASE [Garden] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Garden] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Garden] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Garden] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Garden] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Garden] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Garden] SET QUERY_STORE = ON
GO
ALTER DATABASE [Garden] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [Garden]
GO
/****** Object:  Table [dbo].[crop_group]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[crop_group](
	[crop_group_ID] [int] NOT NULL,
	[common_name] [varchar](50) NOT NULL,
	[scientific_name] [varchar](50) NULL,
	[crop_nitrogren_level] [int] NOT NULL,
	[example_plants] [varchar](250) NULL,
PRIMARY KEY CLUSTERED 
(
	[crop_group_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[frost_tolerance]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[frost_tolerance](
	[frost_tolerance_ID] [int] NOT NULL,
	[frost_tolerance_text] [varchar](50) NOT NULL,
	[frost_tolerance_detail] [varchar](250) NULL,
PRIMARY KEY CLUSTERED 
(
	[frost_tolerance_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurement_unit]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[measurement_unit](
	[measurement_unit_ID] [int] NOT NULL,
	[measurement_unit_text] [varchar](15) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[measurement_unit_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[my_season]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[my_season](
	[my_season_ID] [int] IDENTITY(1,1) NOT NULL,
	[my_season_text] [varchar](15) NOT NULL,
	[my_season_year] [int] NULL,
	[season_active] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[my_season_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant](
	[plant_ID] [int] IDENTITY(1,1) NOT NULL,
	[plant_name] [varchar](50) NOT NULL,
	[plant_in_spring] [bit] NULL,
	[plant_in_fall] [bit] NULL,
	[days_to_harvest] [int] NULL,
	[space_required_seedling] [int] NULL,
	[space_required_seeds] [int] NULL,
	[depth_requirement] [int] NULL,
	[depth_to_plant_seeds] [decimal](6, 2) NULL,
	[times_succeeded] [float] NULL,
	[total_times_planted] [float] NULL,
	[plant_active] [bit] NULL,
	[always_include] [bit] NULL,
	[crop_group_ID] [int] NULL,
	[sun_ID] [int] NULL,
	[soil_moisture_ID] [int] NULL,
	[frost_tolerance_ID] [int] NULL,
	[watering_requirement_ID] [int] NULL,
	[indoors_date_range_ID] [int] NULL,
	[seeds_date_range_ID] [int] NULL,
	[seedlings_date_range_ID] [int] NULL,
	[fall_date_range_ID] [int] NULL,
 CONSTRAINT [PK__plant__A571C7DC953CFCAE] PRIMARY KEY CLUSTERED 
(
	[plant_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant_fall_date_range]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant_fall_date_range](
	[fall_date_range_ID] [int] NOT NULL,
	[fall_date_range_label] [varchar](50) NULL,
	[fall_start_date] [date] NULL,
	[fall_end_date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[fall_date_range_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant_indoors_date_range]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant_indoors_date_range](
	[indoors_date_range_ID] [int] NOT NULL,
	[indoors_date_range_label] [varchar](50) NULL,
	[indoors_start_date] [date] NULL,
	[indoors_end_date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[indoors_date_range_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant_seedlings_date_range]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant_seedlings_date_range](
	[seedlings_date_range_ID] [int] NOT NULL,
	[seedlings_date_range_label] [varchar](50) NULL,
	[seedlings_start_date] [date] NULL,
	[seedlings_end_date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[seedlings_date_range_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant_seeds_date_range]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant_seeds_date_range](
	[seeds_date_range_ID] [int] NOT NULL,
	[seeds_date_range_label] [varchar](50) NULL,
	[seeds_start_date] [date] NULL,
	[seeds_end_date] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[seeds_date_range_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plant_set]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plant_set](
	[plant_set_ID] [int] IDENTITY(1,1) NOT NULL,
	[set_quantity] [int] NOT NULL,
	[planted_date] [date] NULL,
	[first_harvest_date] [date] NULL,
	[last_harvest_date] [date] NULL,
	[outcome] [bit] NULL,
	[fixed_location] [bit] NULL,
	[plant_set_notes] [varchar](250) NULL,
	[plant_ID] [int] NOT NULL,
	[my_season_ID] [int] NOT NULL,
	[plot_ID] [int] NOT NULL,
	[set_type_ID] [int] NOT NULL,
 CONSTRAINT [PK__plant_se__27B090A36CF4EFFC] PRIMARY KEY CLUSTERED 
(
	[plant_set_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plot]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plot](
	[plot_ID] [int] NOT NULL,
	[plot_size] [int] NULL,
	[is_container] [bit] NULL,
	[container_depth] [decimal](6, 2) NULL,
	[plot_active] [bit] NULL,
	[plot_nitrogen_level] [int] NULL,
	[zone_ID] [int] NOT NULL,
	[measurement_unit_ID] [int] NULL,
	[sun_ID] [int] NULL,
	[soil_moisture_ID] [int] NULL,
	[plot_row] [int] NULL,
	[plot_column] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[plot_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[set_type]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[set_type](
	[set_type_ID] [int] NOT NULL,
	[set_type_text] [varchar](15) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[set_type_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[soil_moisture]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[soil_moisture](
	[soil_moisture_ID] [int] NOT NULL,
	[soil_moisture_text] [varchar](50) NOT NULL,
	[soil_moisture_detail] [varchar](250) NULL,
PRIMARY KEY CLUSTERED 
(
	[soil_moisture_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[sun]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[sun](
	[sun_ID] [int] NOT NULL,
	[sun_text] [varchar](50) NOT NULL,
	[sun_detail] [varchar](250) NULL,
PRIMARY KEY CLUSTERED 
(
	[sun_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[watering_requirement]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[watering_requirement](
	[watering_requirement_ID] [int] NOT NULL,
	[watering_requirement_text] [varchar](50) NOT NULL,
	[watering_requirement_detail] [varchar](250) NULL,
PRIMARY KEY CLUSTERED 
(
	[watering_requirement_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[zone]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zone](
	[zone_ID] [int] IDENTITY(1,1) NOT NULL,
	[zone_name] [varchar](50) NOT NULL,
	[zone_notes] [varchar](250) NULL,
	[zone_rows] [int] NULL,
	[zone_columns] [int] NULL,
	[zone_is_full] [bit] NULL,
	[zone_active] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[zone_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (1, N'Onion', N'Alliaceae', -1, N'garlic, leek, onion, shallot')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (2, N'Pea & Bean', N'Leguminosae', 3, N'beans, peas')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (3, N'Cabbage', N'Brassicaceae', -3, N'arugula, broccoli, brussles sprout, cabbage, radish, turnip')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (4, N'Nightshade', N'Solanaceae', -2, N'eggplant, peppers, potato, tomato')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (5, N'Carrot', N'Umbelliferae', -1, N'carrot, celery, cilantro, dill, parsnip, parsley')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (6, N'Marrow', N'Cucurbitaceae', -3, N'cucumber, melon, pumpkin, squash, zucchini')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (7, N'Beetroot', N'Chenopodiacaea', -1, N'beets, swiss chard, spinach')
INSERT [dbo].[crop_group] ([crop_group_ID], [common_name], [scientific_name], [crop_nitrogren_level], [example_plants]) VALUES (8, N'Non-rotation', N'Miscellaneous', 0, N'basil, endive, lettuce, okra, sweet corn')
GO
INSERT [dbo].[frost_tolerance] ([frost_tolerance_ID], [frost_tolerance_text], [frost_tolerance_detail]) VALUES (1, N'Cold Hardy', N'Lowest temp 25 degrees F / -3 degrees C')
INSERT [dbo].[frost_tolerance] ([frost_tolerance_ID], [frost_tolerance_text], [frost_tolerance_detail]) VALUES (2, N'Frost Tolerant', N'Lowest temp 32 degrees F / 0 degree C')
INSERT [dbo].[frost_tolerance] ([frost_tolerance_ID], [frost_tolerance_text], [frost_tolerance_detail]) VALUES (3, N'Cold Sensitive', N'Lowest temp 40 degrees F / 4 degrees C')
INSERT [dbo].[frost_tolerance] ([frost_tolerance_ID], [frost_tolerance_text], [frost_tolerance_detail]) VALUES (4, N'Warm Loving', N'Lowest temp 50 degrees F / 10 degrees C')
GO
INSERT [dbo].[measurement_unit] ([measurement_unit_ID], [measurement_unit_text]) VALUES (1, N'Inches')
INSERT [dbo].[measurement_unit] ([measurement_unit_ID], [measurement_unit_text]) VALUES (2, N'Feet')
GO
SET IDENTITY_INSERT [dbo].[my_season] ON 

INSERT [dbo].[my_season] ([my_season_ID], [my_season_text], [my_season_year], [season_active]) VALUES (1, N'Spring24', 2024, 1)
INSERT [dbo].[my_season] ([my_season_ID], [my_season_text], [my_season_year], [season_active]) VALUES (2, N'Fall24', 2024, 1)
INSERT [dbo].[my_season] ([my_season_ID], [my_season_text], [my_season_year], [season_active]) VALUES (3, N'Spring25', 2025, 1)
SET IDENTITY_INSERT [dbo].[my_season] OFF
GO
SET IDENTITY_INSERT [dbo].[plant] ON 

INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (4, N'Lettuce', 1, 1, 30, 6, 6, 6, CAST(1.00 AS Decimal(6, 2)), 1, 4, 1, 1, 8, 2, 2, 2, 3, 7, 1, 2, 4)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (5, N'Garlic', 0, 1, 180, 6, 6, 12, CAST(4.00 AS Decimal(6, 2)), NULL, 4, 1, 0, 1, 1, 2, 1, 1, NULL, NULL, NULL, 19)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (7, N'Pepper', 1, 0, 120, 18, 18, 12, CAST(1.00 AS Decimal(6, 2)), NULL, 1, 1, 0, 4, 1, 2, 4, 2, 3, NULL, 7, NULL)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (8, N'Arugula', 1, 1, 45, 6, 10, 6, CAST(0.00 AS Decimal(6, 2)), NULL, 1, 1, 0, 3, 1, 2, 3, 2, 7, 2, 1, 3)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (9, N'Basil', 1, 0, 120, 18, 12, 6, CAST(0.00 AS Decimal(6, 2)), NULL, 0, 1, 1, 8, 3, 2, 3, 2, 8, 8, 7, NULL)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (10, N'Broccoli', 1, 1, 90, 12, 20, 6, CAST(0.00 AS Decimal(6, 2)), NULL, 0, 1, 0, 3, 1, 2, 2, 3, 7, 2, 2, 1)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (12, N'Carrot', 1, 1, 80, 3, 12, 18, CAST(0.00 AS Decimal(6, 2)), NULL, 1, 1, 0, 5, 2, 2, 3, 3, NULL, 2, NULL, 5)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (15, N'Asparagus', 1, 0, 425, 72, 72, 36, CAST(1.00 AS Decimal(6, 2)), NULL, 0, 1, 1, 8, 1, 2, 4, 2, NULL, 4, NULL, NULL)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (21, N'Cucumber', 1, 0, 120, 36, 36, 12, CAST(1.00 AS Decimal(6, 2)), NULL, 0, 1, NULL, 6, 1, 3, 3, 3, NULL, NULL, NULL, NULL)
INSERT [dbo].[plant] ([plant_ID], [plant_name], [plant_in_spring], [plant_in_fall], [days_to_harvest], [space_required_seedling], [space_required_seeds], [depth_requirement], [depth_to_plant_seeds], [times_succeeded], [total_times_planted], [plant_active], [always_include], [crop_group_ID], [sun_ID], [soil_moisture_ID], [frost_tolerance_ID], [watering_requirement_ID], [indoors_date_range_ID], [seeds_date_range_ID], [seedlings_date_range_ID], [fall_date_range_ID]) VALUES (27, N'Green Bean', 1, 0, 55, 8, 18, 8, CAST(1.00 AS Decimal(6, 2)), NULL, 0, 1, NULL, 2, 1, 2, 3, 3, NULL, NULL, NULL, NULL)
SET IDENTITY_INSERT [dbo].[plant] OFF
GO
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (1, N'Planting Week 1', NULL, NULL)
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (2, N'Planting Week 2', NULL, NULL)
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (3, N'Planting Week 3', NULL, NULL)
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (4, N'Planting Week 4', CAST(N'2024-07-27' AS Date), CAST(N'2024-08-10' AS Date))
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (5, N'Planting Week 5', NULL, NULL)
INSERT [dbo].[plant_fall_date_range] ([fall_date_range_ID], [fall_date_range_label], [fall_start_date], [fall_end_date]) VALUES (19, N'Planting Week 19', CAST(N'2024-10-19' AS Date), CAST(N'2024-11-02' AS Date))
GO
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (1, N'Planting Week 1', NULL, NULL)
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (2, N'Planting Week 2', NULL, NULL)
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (3, N'Planting Week 3', NULL, NULL)
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (4, N'Planting Week 4', CAST(N'2024-02-27' AS Date), CAST(N'2024-03-14' AS Date))
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (7, N'Planting Week 7', CAST(N'2024-03-27' AS Date), CAST(N'2024-04-10' AS Date))
INSERT [dbo].[plant_indoors_date_range] ([indoors_date_range_ID], [indoors_date_range_label], [indoors_start_date], [indoors_end_date]) VALUES (8, N'Planting Week 8', NULL, NULL)
GO
INSERT [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID], [seedlings_date_range_label], [seedlings_start_date], [seedlings_end_date]) VALUES (1, N'Planting Week 1', NULL, NULL)
INSERT [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID], [seedlings_date_range_label], [seedlings_start_date], [seedlings_end_date]) VALUES (2, N'Planting Week 2', CAST(N'2024-04-17' AS Date), CAST(N'2024-04-24' AS Date))
INSERT [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID], [seedlings_date_range_label], [seedlings_start_date], [seedlings_end_date]) VALUES (3, N'Planting Week 3', NULL, NULL)
INSERT [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID], [seedlings_date_range_label], [seedlings_start_date], [seedlings_end_date]) VALUES (4, N'Planting Week 4', NULL, NULL)
INSERT [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID], [seedlings_date_range_label], [seedlings_start_date], [seedlings_end_date]) VALUES (7, N'Planting Week 7', CAST(N'2024-05-22' AS Date), CAST(N'2024-05-29' AS Date))
GO
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (1, N'Planting Week 1', CAST(N'2024-04-10' AS Date), CAST(N'2024-04-17' AS Date))
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (2, N'Planting Week 2', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (3, N'Planting Week 3', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (4, N'Planting Week 4', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (5, N'Planting Week 5', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (6, N'Planting Week 6', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (7, N'Planting Week 7', NULL, NULL)
INSERT [dbo].[plant_seeds_date_range] ([seeds_date_range_ID], [seeds_date_range_label], [seeds_start_date], [seeds_end_date]) VALUES (8, N'Planting Week 8', NULL, NULL)
GO
SET IDENTITY_INSERT [dbo].[plant_set] ON 

INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (3, 1, CAST(N'2024-11-01' AS Date), NULL, NULL, NULL, 0, NULL, 5, 2, 2, 3)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (4, 1, CAST(N'2024-05-01' AS Date), CAST(N'2024-07-01' AS Date), CAST(N'2024-08-01' AS Date), 1, 0, NULL, 4, 1, 6, 1)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (5, 1, CAST(N'2024-08-01' AS Date), CAST(N'2024-09-01' AS Date), CAST(N'2024-10-15' AS Date), 0, 0, NULL, 4, 2, 3, 2)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (6, 2, CAST(N'2024-05-01' AS Date), NULL, NULL, NULL, 0, NULL, 7, 1, 4, 1)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (7, 4, CAST(N'2024-04-15' AS Date), NULL, NULL, NULL, 0, N'Hello!', 8, 1, 1, 1)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (8, 1, CAST(N'2024-05-22' AS Date), NULL, NULL, NULL, 0, NULL, 12, 1, 4, 2)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (9, 1, NULL, NULL, NULL, NULL, NULL, NULL, 5, 1, 3, 1)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (10, 1, NULL, NULL, NULL, NULL, NULL, NULL, 5, 1, 5, 3)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (11, 1, NULL, NULL, NULL, NULL, NULL, NULL, 4, 1, 10, 1)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (12, 1, NULL, NULL, NULL, NULL, NULL, NULL, 5, 1, 11, 3)
INSERT [dbo].[plant_set] ([plant_set_ID], [set_quantity], [planted_date], [first_harvest_date], [last_harvest_date], [outcome], [fixed_location], [plant_set_notes], [plant_ID], [my_season_ID], [plot_ID], [set_type_ID]) VALUES (13, 1, NULL, NULL, NULL, NULL, NULL, NULL, 4, 2, 10, 1)
SET IDENTITY_INSERT [dbo].[plant_set] OFF
GO
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (1, 6, 0, NULL, 1, 3, 1, 1, 1, 2, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (2, 6, 0, NULL, 1, 3, 1, 1, 1, 3, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (3, 6, 0, NULL, 1, 3, 1, 1, 1, 2, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (4, 6, 0, NULL, 1, 4, 1, 1, 1, 2, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (5, 6, 0, NULL, 1, 3, 1, 1, 1, 2, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (6, 6, 0, NULL, 1, 3, 1, 1, 1, 2, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (7, 6, 0, NULL, 1, 3, 1, 1, 2, 3, NULL, NULL)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (8, 3, 0, NULL, 1, 3, 1, 1, 2, 3, 3, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (9, 9, 0, NULL, 1, 3, 1, 1, 2, 3, 3, 3)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (10, 12, 1, CAST(12.00 AS Decimal(6, 2)), 1, 3, 2, 1, 2, 2, 1, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (11, 9, 0, NULL, 1, 3, 1, 1, 1, 2, 1, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (12, 9, 0, NULL, 1, 3, 1, 1, 1, 2, 1, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (13, 9, 0, NULL, 1, 3, 1, 1, 1, 2, 1, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (14, 9, 0, NULL, 1, 3, 1, 1, 1, 2, 2, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (15, 9, 0, NULL, 1, 3, 1, 1, 1, 2, 2, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (16, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 2, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (17, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 2, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (18, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 2, 3)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (19, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 3, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (20, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 3, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (21, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 3, 3)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (22, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 4, 1)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (23, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 4, 2)
INSERT [dbo].[plot] ([plot_ID], [plot_size], [is_container], [container_depth], [plot_active], [plot_nitrogen_level], [zone_ID], [measurement_unit_ID], [sun_ID], [soil_moisture_ID], [plot_row], [plot_column]) VALUES (24, 6, 0, NULL, 1, 3, 1, 1, 1, 2, 4, 3)
GO
INSERT [dbo].[set_type] ([set_type_ID], [set_type_text]) VALUES (1, N'Seedling(s)')
INSERT [dbo].[set_type] ([set_type_ID], [set_type_text]) VALUES (2, N'Seeds')
INSERT [dbo].[set_type] ([set_type_ID], [set_type_text]) VALUES (3, N'Bulb(s)')
GO
INSERT [dbo].[soil_moisture] ([soil_moisture_ID], [soil_moisture_text], [soil_moisture_detail]) VALUES (1, N'Extrememly Dry', N'0-20%')
INSERT [dbo].[soil_moisture] ([soil_moisture_ID], [soil_moisture_text], [soil_moisture_detail]) VALUES (2, N'Well Drained', N'21-40%')
INSERT [dbo].[soil_moisture] ([soil_moisture_ID], [soil_moisture_text], [soil_moisture_detail]) VALUES (3, N'Moist', N'41-60%')
INSERT [dbo].[soil_moisture] ([soil_moisture_ID], [soil_moisture_text], [soil_moisture_detail]) VALUES (4, N'Wet', N'61-80%')
GO
INSERT [dbo].[sun] ([sun_ID], [sun_text], [sun_detail]) VALUES (1, N'Full', N'6-8 hours')
INSERT [dbo].[sun] ([sun_ID], [sun_text], [sun_detail]) VALUES (2, N'Partial', N'4-6 hours')
INSERT [dbo].[sun] ([sun_ID], [sun_text], [sun_detail]) VALUES (3, N'Shade', N'2-4 hours')
GO
INSERT [dbo].[watering_requirement] ([watering_requirement_ID], [watering_requirement_text], [watering_requirement_detail]) VALUES (1, N'Low', N'1x every other week')
INSERT [dbo].[watering_requirement] ([watering_requirement_ID], [watering_requirement_text], [watering_requirement_detail]) VALUES (2, N'Medium', N'1x per week')
INSERT [dbo].[watering_requirement] ([watering_requirement_ID], [watering_requirement_text], [watering_requirement_detail]) VALUES (3, N'High', N'2x per week')
GO
SET IDENTITY_INSERT [dbo].[zone] ON 

INSERT [dbo].[zone] ([zone_ID], [zone_name], [zone_notes], [zone_rows], [zone_columns], [zone_is_full], [zone_active]) VALUES (1, N'Long raised bed', NULL, 16, 6, 0, 1)
INSERT [dbo].[zone] ([zone_ID], [zone_name], [zone_notes], [zone_rows], [zone_columns], [zone_is_full], [zone_active]) VALUES (2, N'White Flowerpot 1', NULL, 1, 1, 0, 1)
INSERT [dbo].[zone] ([zone_ID], [zone_name], [zone_notes], [zone_rows], [zone_columns], [zone_is_full], [zone_active]) VALUES (5, N'White Flowerpot 2', N'
', 1, 1, 0, 1)
SET IDENTITY_INSERT [dbo].[zone] OFF
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__crop_grou__5070F446] FOREIGN KEY([crop_group_ID])
REFERENCES [dbo].[crop_group] ([crop_group_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__crop_grou__5070F446]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__fall_date__5812160E] FOREIGN KEY([fall_date_range_ID])
REFERENCES [dbo].[plant_fall_date_range] ([fall_date_range_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__fall_date__5812160E]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__frost_tol__534D60F1] FOREIGN KEY([frost_tolerance_ID])
REFERENCES [dbo].[frost_tolerance] ([frost_tolerance_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__frost_tol__534D60F1]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__indoors_d__5535A963] FOREIGN KEY([indoors_date_range_ID])
REFERENCES [dbo].[plant_indoors_date_range] ([indoors_date_range_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__indoors_d__5535A963]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__seedlings__571DF1D5] FOREIGN KEY([seedlings_date_range_ID])
REFERENCES [dbo].[plant_seedlings_date_range] ([seedlings_date_range_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__seedlings__571DF1D5]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__seeds_dat__5629CD9C] FOREIGN KEY([seeds_date_range_ID])
REFERENCES [dbo].[plant_seeds_date_range] ([seeds_date_range_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__seeds_dat__5629CD9C]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__soil_mois__52593CB8] FOREIGN KEY([soil_moisture_ID])
REFERENCES [dbo].[soil_moisture] ([soil_moisture_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__soil_mois__52593CB8]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__sun_ID__5165187F] FOREIGN KEY([sun_ID])
REFERENCES [dbo].[sun] ([sun_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__sun_ID__5165187F]
GO
ALTER TABLE [dbo].[plant]  WITH CHECK ADD  CONSTRAINT [FK__plant__watering___5441852A] FOREIGN KEY([watering_requirement_ID])
REFERENCES [dbo].[watering_requirement] ([watering_requirement_ID])
GO
ALTER TABLE [dbo].[plant] CHECK CONSTRAINT [FK__plant__watering___5441852A]
GO
ALTER TABLE [dbo].[plant_set]  WITH CHECK ADD  CONSTRAINT [FK__plant_set__my_se__619B8048] FOREIGN KEY([my_season_ID])
REFERENCES [dbo].[my_season] ([my_season_ID])
GO
ALTER TABLE [dbo].[plant_set] CHECK CONSTRAINT [FK__plant_set__my_se__619B8048]
GO
ALTER TABLE [dbo].[plant_set]  WITH CHECK ADD  CONSTRAINT [FK__plant_set__plant__60A75C0F] FOREIGN KEY([plant_ID])
REFERENCES [dbo].[plant] ([plant_ID])
GO
ALTER TABLE [dbo].[plant_set] CHECK CONSTRAINT [FK__plant_set__plant__60A75C0F]
GO
ALTER TABLE [dbo].[plant_set]  WITH CHECK ADD  CONSTRAINT [FK__plant_set__plot___628FA481] FOREIGN KEY([plot_ID])
REFERENCES [dbo].[plot] ([plot_ID])
GO
ALTER TABLE [dbo].[plant_set] CHECK CONSTRAINT [FK__plant_set__plot___628FA481]
GO
ALTER TABLE [dbo].[plant_set]  WITH CHECK ADD  CONSTRAINT [FK__plant_set__set_t__6383C8BA] FOREIGN KEY([set_type_ID])
REFERENCES [dbo].[set_type] ([set_type_ID])
GO
ALTER TABLE [dbo].[plant_set] CHECK CONSTRAINT [FK__plant_set__set_t__6383C8BA]
GO
ALTER TABLE [dbo].[plot]  WITH CHECK ADD FOREIGN KEY([measurement_unit_ID])
REFERENCES [dbo].[measurement_unit] ([measurement_unit_ID])
GO
ALTER TABLE [dbo].[plot]  WITH CHECK ADD FOREIGN KEY([soil_moisture_ID])
REFERENCES [dbo].[soil_moisture] ([soil_moisture_ID])
GO
ALTER TABLE [dbo].[plot]  WITH CHECK ADD FOREIGN KEY([sun_ID])
REFERENCES [dbo].[sun] ([sun_ID])
GO
ALTER TABLE [dbo].[plot]  WITH CHECK ADD FOREIGN KEY([zone_ID])
REFERENCES [dbo].[zone] ([zone_ID])
GO
/****** Object:  StoredProcedure [dbo].[AddPlant]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/* CREATE STORED PRODECURES TO ADD DATA */

CREATE PROCEDURE [dbo].[AddPlant]
   @plant_name VARCHAR(50),
   @plant_in_spring bit,
   @plant_in_fall bit,
   @days_to_harvest int,
   @space_required_seedling int,
   @space_required_seeds int,
   @depth_requirement int,
   @depth_to_plant_seeds int,
   @always_include bit,
   @crop_group_ID int,
   @sun_ID int,
   @soil_moisture_ID int,
   @frost_tolerance_ID int,
   @watering_requirement_ID int,
   @indoors_date_range_ID int,
   @seeds_date_range_ID int,
   @seedlings_date_range_ID int,
   @fall_date_range_ID int 
AS
BEGIN
INSERT INTO plant (
   plant_name, 
   plant_in_spring, 
   plant_in_fall,
   days_to_harvest,
   space_required_seedling,
   space_required_seeds,
   depth_requirement,
   depth_to_plant_seeds,
   always_include,
   crop_group_ID,
   sun_ID,
   soil_moisture_ID,
   frost_tolerance_ID,
   watering_requirement_ID,
   indoors_date_range_ID,
   seeds_date_range_ID,
   seedlings_date_range_ID,
   fall_date_range_ID,
   total_times_planted,
   plant_active,
   times_succeeded)
VALUES (
   @plant_name,
   @plant_in_spring,
   @plant_in_fall,
   @days_to_harvest,
   @space_required_seedling,
   @space_required_seeds,
   @depth_requirement,
   @depth_to_plant_seeds,
   @always_include,
   @crop_group_ID,
   @sun_ID,
   @soil_moisture_ID,
   @frost_tolerance_ID,
   @watering_requirement_ID,
   @indoors_date_range_ID,
   @seeds_date_range_ID,
   @seedlings_date_range_ID,
   @fall_date_range_ID,
   '0',
   '1',
   NULL);
END;  
GO
/****** Object:  StoredProcedure [dbo].[AddPlantSet]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddPlantSet]
   @set_quantity int,
   @plant_ID int,
   @my_season_ID int,
   @plot_ID int,
   @set_type_ID int
AS
BEGIN
INSERT INTO plant_set (
   set_quantity,
   plant_ID,
   my_season_ID,
   plot_ID,
   set_type_ID)
VALUES (
   @set_quantity,
   @plant_ID,
   @my_season_ID,
   @plot_ID,
   @set_type_ID);

UPDATE plant 
SET total_times_planted = 
   ((SELECT total_times_planted 
     FROM plant 
	 WHERE plant_ID = @plant_ID) 
	 + 1)
WHERE plant_ID = @plant_ID

END;
GO
/****** Object:  StoredProcedure [dbo].[AddPlot]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddPlot] 
   @plot_id int,
   @plot_size int, 
   @measurement_unit_id int,
   @is_container int, 
   @container_depth int, 
   @zone_id int,
   @sun_id int,
   @soil_moisture_id int,
   @plot_row int,
   @plot_column int

AS
BEGIN
INSERT INTO plot (
   plot_ID, 
   plot_size, 
   measurement_unit_id, 
   is_container, 
   container_depth, 
   zone_id, sun_ID, 
   soil_moisture_ID, 
   plot_row,
   plot_column,
   plot_nitrogen_level, 
   plot_active)
VALUES
   (@plot_id, 
   @plot_size, 
   @measurement_unit_id, 
   @is_container, 
   @container_depth, 
   @zone_id, @sun_id, 
   @soil_moisture_id, 
   @plot_row,
   @plot_column,
   '3', 
   '1');
END;
GO
/****** Object:  StoredProcedure [dbo].[AddWeekFall]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddWeekFall] 
   @week_number int
AS
BEGIN
DECLARE @week_char VARCHAR(2)
DECLARE @week_string VARCHAR(20)

SET @week_char=CONVERT(VARCHAR(2), @week_number)
SET @week_string='Planting Week ' + @week_char

INSERT INTO plant_fall_date_range 
   (fall_date_range_ID, fall_date_range_label)
VALUES
   (@week_number, @week_string);
END;
GO
/****** Object:  StoredProcedure [dbo].[AddWeekIndoors]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddWeekIndoors] 
   @week_number int
AS
BEGIN
DECLARE @week_char VARCHAR(2)
DECLARE @week_string VARCHAR(20)

SET @week_char=CONVERT(VARCHAR(2), @week_number)
SET @week_string='Planting Week ' + @week_char

INSERT INTO plant_indoors_date_range 
   (indoors_date_range_ID, indoors_date_range_label)
VALUES
   (@week_number, @week_string);
END;
GO
/****** Object:  StoredProcedure [dbo].[AddWeekSeedlings]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddWeekSeedlings] 
   @week_number int
AS
BEGIN
DECLARE @week_char VARCHAR(2)
DECLARE @week_string VARCHAR(20)

SET @week_char=CONVERT(VARCHAR(2), @week_number)
SET @week_string='Planting Week ' + @week_char

INSERT INTO plant_seedlings_date_range 
   (seedlings_date_range_ID, seedlings_date_range_label)
VALUES
   (@week_number, @week_string);
END;
GO
/****** Object:  StoredProcedure [dbo].[AddWeekSeeds]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddWeekSeeds] 
   @week_number int
AS
BEGIN
DECLARE @week_char VARCHAR(2)
DECLARE @week_string VARCHAR(20)

SET @week_char=CONVERT(VARCHAR(2), @week_number)
SET @week_string='Planting Week ' + @week_char

INSERT INTO plant_seeds_date_range 
   (seeds_date_range_ID, seeds_date_range_label)
VALUES
   (@week_number, @week_string);
END;
GO
/****** Object:  StoredProcedure [dbo].[AddZone]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[AddZone] 
   @zone_name VARCHAR(50), 
   @zone_rows int, 
   @zone_columns int, 
   @zone_notes VARCHAR(250)
AS
BEGIN
INSERT INTO zone 
   (zone_name, 
   zone_rows, 
   zone_columns, 
   zone_notes, 
   zone_is_full, 
   zone_active)
VALUES (
   @zone_name, 
   @zone_rows, 
   @zone_columns, 
   @zone_notes, 
   '0', 
   '1');
END;
GO
/****** Object:  StoredProcedure [dbo].[QueryAllPlantsSetupDetail]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[QueryAllPlantsSetupDetail]
AS
SELECT DISTINCT
   plant.plant_ID as 'Plant ID', 
   plant_name as 'Plant Name',
   IIF(ps.my_season_ID>0, 'Yes', 'No') as 'In Plan?',
   common_name as 'Crop Rotation Group', 
   sun_detail as 'Sun Requirement',  
   soil_moisture_text as 'Soil Moisture Requirement', 
   space_required_seeds as 'Space Required For Seeds (inches)', 
   space_required_seedling as 'Space Required Per Seedling (inches)', 
   depth_requirement as 'Depth Requirement (inches)',  
   watering_requirement_detail as 'Watering Requirement',
   frost_tolerance_text as 'Frost Tolerance',
   days_to_harvest as 'Days to Harvest', 
   IIF(plant_in_spring=1, 'Yes', (IIF(plant_in_spring=0, 'No', NULL))) 
     as 'Plant in Spring',
   IIF(plant_in_fall=1, 'Yes', (IIF(plant_in_fall=0, 'No', NULL))) 
      as 'Plant in Fall', 
   COALESCE(CONVERT(VARCHAR(15), indoors_start_date), 'N/A') 
      as 'Start Seeds Indoors', 
   COALESCE(CONVERT(VARCHAR(15), indoors_end_date), 'N/A') 
      as 'Finish Seeds Indoors', 
   COALESCE(CONVERT(VARCHAR(15), seeds_start_date), 'N/A') 
      as 'Start Seeds Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seeds_end_date), 'N/A') 
      as 'Finish Seeds Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seedlings_start_date), 'N/A') 
      as 'Start Seedlings Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seedlings_end_date), 'N/A') 
      as 'Finish Seedlings Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), fall_start_date), 'N/A') 
      as 'Start All Fall', 
   COALESCE(CONVERT(VARCHAR(15), fall_end_date), 'N/A') 
      as 'Finish All Fall'
FROM plant
LEFT JOIN sun
ON plant.sun_ID = sun.sun_ID
LEFT JOIN soil_moisture as sm
ON plant.soil_moisture_ID = sm.soil_moisture_ID
LEFT JOIN frost_tolerance as ft
ON plant.frost_tolerance_ID = ft.frost_tolerance_ID
LEFT JOIN watering_requirement as wr
ON plant.watering_requirement_ID = wr.watering_requirement_ID
LEFT JOIN crop_group as cg
ON plant.crop_group_ID = cg.crop_group_ID
LEFT JOIN plant_indoors_date_range as indoors
ON plant.indoors_date_range_ID = indoors.indoors_date_range_ID
LEFT JOIN plant_seeds_date_range as seeds
ON plant.seeds_date_range_ID = seeds.seeds_date_range_ID
LEFT JOIN plant_seedlings_date_range as seedlings
ON plant.seedlings_date_range_ID = seedlings.seedlings_date_range_ID
LEFT JOIN plant_fall_date_range as fall
ON plant.fall_date_range_ID = fall.fall_date_range_ID
LEFT JOIN plant_set as ps
ON plant.plant_ID = ps.plant_ID
LEFT JOIN my_season as ms
ON ps.my_season_ID = ms.my_season_ID

ORDER BY [In Plan?] DESC, [Crop Rotation Group], [Plant Name] ASC



GO
/****** Object:  StoredProcedure [dbo].[QueryOutcomeDetail]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[QueryOutcomeDetail]
AS

SELECT plant_set_ID as 'Plant Set ID', my_season_text AS 'Season',  
plant_name AS 'Plant', zone_name AS 'Zone', plot.plot_ID as 'Plot Number', 
set_quantity AS 'Quantity', set_type_text AS 'Set Type', planted_date as 'Date Planted',  
first_harvest_date AS 'First Harvest', last_harvest_date AS 'Last Harvest', 
IIF(outcome=1, 'Success', (IIF(outcome=0, 'Failure', NULL))) AS 'Outcome'

FROM plant_set as ps
LEFT JOIN plant
ON ps.plant_ID = plant.plant_ID
LEFT JOIN my_season as ms
ON ps.my_season_ID = ms.my_season_ID
LEFT JOIN plot
ON ps.plot_ID = plot.plot_ID
LEFT JOIN zone
ON plot.zone_ID = zone.zone_ID
LEFT JOIN set_type as st
ON ps.set_type_ID = st.set_type_ID

ORDER BY [Date Planted]

GO
/****** Object:  StoredProcedure [dbo].[QueryOutcomeSummary]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[QueryOutcomeSummary]
AS

;WITH LastPlanted AS (
   SELECT *,
      ROW_NUMBER() OVER (
	     PARTITION BY plant_set.plant_ID 
		 ORDER BY planted_date DESC) as row_number
	FROM plant_set
	)

SELECT
   plant_name as 'Plant Name', 
   total_times_planted as 'Times Planted',
   (times_succeeded/total_times_planted*100) 
      as 'Success Ratio ', 
   my_season_text as 'Most Recent Season',
   IIF(outcome = 1, 'Success', 'Failure') as 'Most Recent Outcome'

FROM LastPlanted as lp
LEFT JOIN plant
    ON lp.plant_ID = plant.plant_ID
    LEFT JOIN my_season as ms
    ON lp.my_season_ID = ms.my_season_ID

WHERE outcome IS NOT NULL AND row_number = 1




GO
/****** Object:  StoredProcedure [dbo].[QueryPlantingPlan]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[QueryPlantingPlan]
AS

SELECT 
   ps.my_season_ID as 'Season ID', 
   my_season_text AS 'Season', 
   plant_name AS 'Plant', 
   zone_name AS 'Zone', 
   plot.plot_ID as 'Plot Number', 
   space_required_seeds as 'Space Required For Seeds (inches)', 
   space_required_seedling as 'Space Required Per Seedling (inches)', 
   depth_to_plant_seeds as 'Depth to Plant Seeds (inches)',  
   watering_requirement_detail as 'Watering Requirement',
   days_to_harvest as 'Days to Harvest', 
   COALESCE(CONVERT(VARCHAR(15), indoors_start_date), 'N/A') 
      as 'Start Seeds Indoors', 
   COALESCE(CONVERT(VARCHAR(15), indoors_end_date), 'N/A') 
      as 'Finish Seeds Indoors', 
   COALESCE(CONVERT(VARCHAR(15), seeds_start_date), 'N/A') 
      as 'Start Seeds Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seeds_end_date), 'N/A') 
      as 'Finish Seeds Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seedlings_start_date), 'N/A') 
      as 'Start Seedlings Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), seedlings_end_date), 'N/A') 
      as 'Finish Seedlings Outdoors', 
   COALESCE(CONVERT(VARCHAR(15), fall_start_date), 'N/A') 
      as 'Start All Fall', 
   COALESCE(CONVERT(VARCHAR(15), fall_end_date), 'N/A') 
      as 'Finish All Fall' 

FROM plant_set as ps
LEFT JOIN plant
ON ps.plant_ID = plant.plant_ID
LEFT JOIN my_season as ms
ON ps.my_season_ID = ms.my_season_ID
LEFT JOIN plot
ON ps.plot_ID = plot.plot_ID
LEFT JOIN zone
ON plot.zone_ID = zone.zone_ID
LEFT JOIN plant_indoors_date_range as indoors
ON plant.indoors_date_range_ID = indoors.indoors_date_range_ID
LEFT JOIN plant_seeds_date_range as seeds
ON plant.seeds_date_range_ID = seeds.seeds_date_range_ID
LEFT JOIN plant_seedlings_date_range as seedlings
ON plant.seedlings_date_range_ID = seedlings.seedlings_date_range_ID
LEFT JOIN plant_fall_date_range as fall
ON plant.fall_date_range_ID = fall.fall_date_range_ID
LEFT JOIN watering_requirement as wr
ON plant.watering_requirement_ID = wr.watering_requirement_ID

ORDER BY [Season ID], plot.zone_ID, ps.plot_ID

GO
/****** Object:  StoredProcedure [dbo].[RetrieveCropGroupData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveCropGroupData]
AS
SELECT
	crop_group_ID,
	common_name,
	scientific_name,
	crop_nitrogren_level,
	example_plants
FROM crop_group
GO
/****** Object:  StoredProcedure [dbo].[RetrieveFrostToleranceData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveFrostToleranceData]
AS
SELECT
	frost_tolerance_ID,
	frost_tolerance_text,
	frost_tolerance_detail
FROM frost_tolerance
GO
/****** Object:  StoredProcedure [dbo].[RetrieveMeasurementUnitData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveMeasurementUnitData]
AS
SELECT 
	measurement_unit_ID, 
	measurement_unit_text 
FROM measurement_unit
GO
/****** Object:  StoredProcedure [dbo].[RetrieveMySeasonData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveMySeasonData]
AS
SELECT my_season_ID, my_season_text, my_season_year
FROM my_season
WHERE season_active = 1
GO
/****** Object:  StoredProcedure [dbo].[RetrievePlantNames]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrievePlantNames]

AS 
SELECT plant_ID, plant_name
FROM
plant

ORDER BY plant_name
GO
/****** Object:  StoredProcedure [dbo].[RetrievePlantRequirements]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrievePlantRequirements]
AS
SELECT 
	plant_ID,
	plant_name,
	space_required_seedling,
	space_required_seeds,
	depth_requirement,
	sun_ID,
	soil_moisture_ID,
	crop_nitrogren_level,
	always_include,
	plant_in_spring, 
	plant_in_fall,
	frost_tolerance_ID,
	total_times_planted,
	times_succeeded
FROM
   plant
JOIN 
   crop_group as cg
ON 
   plant.crop_group_ID = cg.crop_group_ID
WHERE 
	plant_active = 1

GO
/****** Object:  StoredProcedure [dbo].[RetrievePlotData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrievePlotData]

AS

SELECT 
	plot_ID,
	plot_size, 
	measurement_unit_ID, 
	is_container, 
	container_depth, 
	plot_nitrogen_level, 
	zone_ID, 
	sun_ID, 
	soil_moisture_ID,
	plot_row,
	plot_column,
	plot_active 
FROM
	plot
GO
/****** Object:  StoredProcedure [dbo].[RetrieveSetTypes]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveSetTypes]

AS 
SELECT set_type_ID, set_type_text
FROM
set_type

ORDER BY set_type_text DESC
GO
/****** Object:  StoredProcedure [dbo].[RetrieveSoilMoistureData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveSoilMoistureData]
AS
SELECT
	soil_moisture_ID,
	(soil_moisture_text + ': ' + soil_moisture_detail) 
	as soil_moisture_info
FROM soil_moisture
GO
/****** Object:  StoredProcedure [dbo].[RetrieveSunData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveSunData]
AS
SELECT
	sun_ID,
	(sun_text + ': ' + sun_detail) 
	as sun_info
FROM sun
GO
/****** Object:  StoredProcedure [dbo].[RetrieveWateringRequirementData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveWateringRequirementData]
AS
SELECT
	watering_requirement_ID,
	(watering_requirement_text + ': ' + watering_requirement_detail)
	as watering_requirement_info
FROM watering_requirement
GO
/****** Object:  StoredProcedure [dbo].[RetrieveZoneData]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[RetrieveZoneData]
AS
SELECT
	zone_ID,
	zone_name,
	zone_rows,
	zone_columns,
	zone_active,
	zone_is_full,
	zone_notes
FROM zone
GO
/****** Object:  StoredProcedure [dbo].[UpdateFallDateRange]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateFallDateRange]
   @fall_date_range_id int,
   @fall_start_date DATE,
   @fall_end_date DATE
AS
BEGIN
UPDATE plant_fall_date_range
SET 
   fall_start_date = @fall_start_date,
   fall_end_date = @fall_end_date
WHERE
   fall_date_range_ID = @fall_date_range_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateIndoorsDateRange]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateIndoorsDateRange]
   @indoors_date_range_id int,
   @indoors_start_date DATE,
   @indoors_end_date DATE
AS
BEGIN
UPDATE plant_indoors_date_range
SET 
   indoors_start_date = @indoors_start_date,
   indoors_end_date = @indoors_end_date
WHERE
   indoors_date_range_ID = @indoors_date_range_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateMySeason]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/* CREATE STORED PRODECURES TO UPDATE OR EDIT DATA */

CREATE PROCEDURE [dbo].[UpdateMySeason]
   @my_season_id int,
   @my_season_text VARCHAR(15),
   @my_season_year int
AS 
BEGIN
UPDATE my_season
SET
   my_season_text = @my_season_text,
   my_season_year = @my_season_year
WHERE
   my_season_ID = @my_season_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdatePlant]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdatePlant]
   @plant_id int,
   @plant_name VARCHAR(50),
   @plant_in_spring bit,
   @plant_in_fall bit,
   @days_to_harvest int,
   @space_required_seedling int,
   @space_required_seeds int,
   @depth_requirement int,
   @depth_to_plant_seeds int,
   @times_succeeded int,
   @total_times_planted int,
   @plant_active bit,
   @always_include bit,
   @crop_group_ID int,
   @sun_ID int,
   @soil_moisture_ID int,
   @frost_tolerance_ID int,
   @watering_requirement_ID int,
   @indoors_date_range_ID int,
   @seeds_date_range_ID int,
   @seedlings_date_range_ID int,
   @fall_date_range_ID int  
AS
BEGIN
UPDATE plant
SET
   plant_name = @plant_name,
   plant_in_spring = @plant_in_spring,
   plant_in_fall = @plant_in_fall,
   days_to_harvest = @days_to_harvest,
   space_required_seedling = @space_required_seedling,
   space_required_seeds = @space_required_seeds,
   depth_requirement = @depth_requirement,
   depth_to_plant_seeds = @depth_to_plant_seeds,
   times_succeeded = @times_succeeded,
   total_times_planted = @total_times_planted,
   plant_active = @plant_active,
   always_include = @always_include,
   crop_group_ID = @crop_group_ID,
   sun_ID = @sun_ID,
   soil_moisture_ID = @soil_moisture_ID,
   frost_tolerance_ID = @frost_tolerance_ID,
   watering_requirement_ID = @watering_requirement_ID,
   indoors_date_range_ID = @indoors_date_range_ID,
   seeds_date_range_ID = @seeds_date_range_ID,
   seedlings_date_range_ID = @seedlings_date_range_ID,
   fall_date_range_ID = @fall_date_range_ID
WHERE plant_ID = @plant_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdatePlantSet]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdatePlantSet]
   @plant_set_id int,
   @set_quantity int,
   @planted_date DATE,
   @first_harvest_date DATE,
   @last_harvest_date DATE,
   @outcome bit,
   @fixed_location bit,
   @plant_ID int,
   @my_season_ID int,
   @plot_ID int,
   @set_type_id int,
   @plant_set_notes VARCHAR(250)
AS
BEGIN
UPDATE plant_set
SET
   set_quantity = @set_quantity,
   planted_date = @planted_date,
   first_harvest_date = @first_harvest_date,
   last_harvest_date = @last_harvest_date,
   outcome = @outcome,
   fixed_location = @fixed_location,
   plant_ID = @plant_ID,
   my_season_ID = @my_season_ID,
   plot_ID = @plot_ID,
   set_type_ID = @set_type_id,
   plant_set_notes = @plant_set_notes
WHERE plant_set_ID = @plant_set_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdatePlot]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdatePlot]
   @plot_id int,
   @plot_size int,
   @measurement_unit_ID int,
   @is_container bit,
   @container_depth decimal(6,2),
   @plot_nitrogen_level int,
   @zone_ID int,   
   @sun_ID int,
   @soil_moisture_ID int,
   @plot_row int,
   @plot_column int,
   @plot_active bit
AS
BEGIN
UPDATE plot
SET
   plot_size = @plot_size,
   measurement_unit_ID = @measurement_unit_ID,
   is_container = @is_container,
   container_depth = @container_depth,
   plot_nitrogen_level = @plot_nitrogen_level,
   zone_ID = @zone_ID,
   sun_ID = @sun_ID,
   soil_moisture_ID = @soil_moisture_ID,
   plot_row = @plot_row,
   plot_column = @plot_column,
   plot_active = @plot_active
WHERE plot_ID = @plot_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateSeedlingsDateRange]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateSeedlingsDateRange]
   @seedlings_date_range_id int,
   @seedlings_start_date DATE,
   @seedlings_end_date DATE
AS
BEGIN
UPDATE plant_seedlings_date_range
SET 
   seedlings_start_date = @seedlings_start_date,
   seedlings_end_date = @seedlings_end_date
WHERE
   seedlings_date_range_ID = @seedlings_date_range_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateSeedsDateRange]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateSeedsDateRange]
   @seeds_date_range_id int,
   @seeds_start_date DATE,
   @seeds_end_date DATE
AS
BEGIN
UPDATE plant_seeds_date_range
SET 
   seeds_start_date = @seeds_start_date,
   seeds_end_date = @seeds_end_date
WHERE
   seeds_date_range_ID = @seeds_date_range_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateWateringRequirement]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateWateringRequirement]
   @watering_requirement_id int,
   @watering_requirement_text varchar(15),
   @watering_requirement_detail varchar(250)
AS
BEGIN
UPDATE watering_requirement
SET
   watering_requirement_text = @watering_requirement_text,
   watering_requirement_detail = @watering_requirement_detail
WHERE 
   watering_requirement_ID = @watering_requirement_id;
END;
GO
/****** Object:  StoredProcedure [dbo].[UpdateZone]    Script Date: 6/24/2024 7:04:28 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[UpdateZone]
   @zone_id int,
   @zone_name VARCHAR(50), 
   @zone_rows int, 
   @zone_columns int, 
   @zone_is_full bit,
   @zone_active bit,
   @zone_notes VARCHAR(250)
AS
BEGIN
UPDATE zone
SET
   zone_name = @zone_name, 
   zone_rows = @zone_rows, 
   zone_columns = @zone_columns, 
   zone_is_full = @zone_is_full,
   zone_active = @zone_active,
   zone_notes = @zone_notes
WHERE zone_ID = @zone_id;
END;
GO
USE [master]
GO
ALTER DATABASE [Garden] SET  READ_WRITE 
GO
